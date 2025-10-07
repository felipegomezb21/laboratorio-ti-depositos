from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from starlette.middleware.wsgi import WSGIMiddleware

from .db import SessionLocal, init_db, Item

# ---- DB Session dependency ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- FastAPI App ----
app = FastAPI(title="Lab Intro API (REST + SOAP)", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

class ItemIn(BaseModel):
    name: str

class ItemOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemIn, db: Session = Depends(get_db)):
    item = Item(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items", response_model=List[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).order_by(Item.id.asc()).all()

# ---- SOAP (Spyne) mounted at /soap ----
from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class SoapItem(ComplexModel):
    __namespace__ = 'urn:lab.soap'
    id = Integer
    name = Unicode

class EchoService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def echo(ctx, s):
        # Simple echo. SoapUI llamará a esta operación.
        return s

    @rpc(Unicode, _returns=SoapItem)
    def create_item(ctx, name):
        db = SessionLocal()
        try:
            item = Item(name=name)
            db.add(item)
            db.commit()
            db.refresh(item)
            return SoapItem(id=item.id, name=item.name)
        finally:
            db.close()

    @rpc(_returns=Array(SoapItem))
    def list_items(ctx):
        db = SessionLocal()
        try:
            items = db.query(Item).order_by(Item.id.asc()).all()
            return [SoapItem(id=item.id, name=item.name) for item in items]
        finally:
            db.close()

soap_app = Application(
    [EchoService],
    tns='urn:lab.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)
app.mount("/soap", WSGIMiddleware(wsgi_app))
