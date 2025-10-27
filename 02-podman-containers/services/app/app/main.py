from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel


app = FastAPI(
    title="Podman Notes API",
    description="API simple para registrar notas y demostrar persistencia con volúmenes.",
    version="0.1.0",
)

DATA_PATH = Path(os.getenv("NOTES_PATH", "/app/data/notes.json"))
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)


class NoteIn(BaseModel):
    text: str


class Note(NoteIn):
    id: int
    created_at: str


def read_notes() -> List[dict]:
    if not DATA_PATH.exists():
        return []
    try:
        with DATA_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def write_notes(notes: List[dict]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2)


@app.on_event("startup")
def startup_event() -> None:
    notes = read_notes()
    print(f"[startup] Notes loaded: {len(notes)}")


@app.get("/")
def root() -> dict:
    return {"message": "Laboratorio 02 - Podman Notes API"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/notes", response_model=List[Note])
def list_notes() -> List[Note]:
    return read_notes()


@app.post("/notes", response_model=Note, status_code=201)
def create_note(payload: NoteIn) -> Note:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El campo text no puede estar vacío.")

    notes = read_notes()
    new_id = (notes[-1]["id"] + 1) if notes else 1
    note = {
        "id": new_id,
        "text": text,
        "created_at": datetime.utcnow().isoformat(),
    }

    notes.append(note)
    write_notes(notes)

    print(f"[notes] Created note {note['id']}: {note['text']}")
    return note


@app.delete("/notes/{note_id}", status_code=204, response_class=Response)
def delete_note(note_id: int) -> Response:
    notes = read_notes()
    updated = [note for note in notes if note["id"] != note_id]
    if len(updated) == len(notes):
        raise HTTPException(status_code=404, detail="Nota no encontrada.")

    write_notes(updated)
    print(f"[notes] Deleted note {note_id}")
    return Response(status_code=204)
