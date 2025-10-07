# Introducción al repo de laboratorios de TI Depositos 

**Objetivo:** Realizar la configuración inicial de las herramientas principales y dependencias necesarias para le desarrollo en general de los laboratorios.

**Requerimientos:** Toda la disposición de aprender y aportar.

## Conceptos Clave

- **WSL2:** Capa de virtualización ligera en Windows que permite ejecutar Linux real y contenedores nativamente sobre windows.  
- **Imagen vs Contenedor:** La imagen es una plantilla inmutable; el contenedor es una instancia viva.  
- **Docker / Podman:** Herramientas para construir y ejecutar contenedores; Ambos son compatibles en cuanto a comandos y opciones.   
- **VSCode:** IDE recomendado con extensiones que ayudan y opensource. Puedes usar el de tu preferencia.
- **Postman:** Herramienta grafica para probar recursos http, como APIs REST.  
- **SoapUI:** Herramienta grafica especializada para probar servicios SOAP. 
- **DBeaver:** Cliente gráfico para explorar y consultar la bases de datos.  

## Paso a paso

Los siguientes pasos que necesitan instalacion de software, requieren permisos de administrador del sistema, por lo que si no administramos la maquina, debemos solicitar instalación a ofimatica.

### 1. Instalación de WSL2 (Solo aplica para windows)

- Abre **PowerShell** como Administrador y ejecuta:
  ```powershell
  wsl --install
  ```
  Reinicia si te lo pide.
- Verifica:
  ```powershell
  wsl --status
  wsl -l -v
  ```
- (Opcional) Define Ubuntu como predeterminada:
  ```powershell
  wsl -s Ubuntu
  ```

### 2. Instalación de Podman (Gratuito)

***Nota: se puede tratar de instalar directamente desde la terminal de wsl**

Tanto Podman, como docker son compatibles y nos permitiran desarrollar las mismas capacidades con el mismo entendimiento en cuento a contenedores. Docker requiere licencia para entornos empresariales.

- Ve a [https://www.postman.com/downloads](https://www.postman.com/downloads).  
- Descarga el instalador para **Windows**.  
- Ejecuta el archivo `.exe` y sigue el asistente (Siguiente → Siguiente → Finalizar).  
- Al finalizar, Postman se abrirá automáticamente.  
- Inicia sesión o selecciona **“Skip and go offline”** para usarlo sin cuenta.  
- Verifica la instalación haciendo consulta de su versión desde la terminal:
```bash
podman version
```
### 3. Instalación de VScode (Gratuito)

***Nota: se puede tratar de instalar directamente desde la terminal de wsl**

- Ve a [https://code.visualstudio.com/](https://code.visualstudio.com/) y descarga el instalador para **Windows**.  
- Ejecuta el archivo `.exe` y sigue el asistente (aceptar → siguiente → instalar).  
- Marca la opción **“Agregar a PATH”** si aparece, para poder usar `code` desde la terminal.  
- Al finalizar, abre VS Code.  
- Verifica la instalación ejecutando en terminal:
  ```bash
  code --version
  ```

## 4. Instalación de Postman (Windows)

1. Ve a [https://www.postman.com/downloads](https://www.postman.com/downloads).  
2. Descarga el instalador para **Windows**.  
3. Ejecuta el archivo `.exe` y completa el asistente.  
4. Al abrir, inicia sesión o selecciona **“Skip and go offline”**.  

## 5. Instalación de DBeaver (Windows)

1. Ve a [https://dbeaver.io/download](https://dbeaver.io/download) y descarga la versión **Community** para Windows.  
2. Ejecuta el instalador `.exe` y sigue los pasos (siguiente → siguiente → finalizar).  
3. Abre DBeaver desde el menú de inicio.

## 6. Instalación de SoapUI (Windows)

1. Ve a [https://www.soapui.org/downloads/soapui/](https://www.soapui.org/downloads/soapui/) y descarga **SoapUI Open Source**.  
2. Ejecuta el instalador `.exe` y sigue el asistente (aceptar licencia → instalar → finalizar).  
3. Abre SoapUI desde el menú de inicio.  
4. Verifica que la ventana principal se abra correctamente y permita importar un WSDL.

### 7. Descargar repo y situarse en el laboratorio

```bash
#Descarga del repositorio a local
git clone git@github.com:nuamx/nmx-png-laboratorio-ti-depositos.git

#Situarse en la carpeta del laboratorio
cd nmx-png-laboratorio-ti-depositos/01-intro-tools
```

### 8. Levantar el stack (Despliegue contenedores App y Base de datos)
Con el siguiente comando realizaremos el build de la aplicación y el despliegue del compose que incluye la aplicación y la base de datos, de acuerdo a nuestro compose.yaml.

```bash
# Con Docker
docker compose up --build

# Con Podman (según tu entorno)
podman compose up --build
```

### 9. Probemos Postman y el API REST

Debemos importar en postman la collección previamente definida para el laboratorio que se encuentra en `labs/postman-collection-lab01.json` y procedemo a ejecutar cada metodo:

- **GET** `http://localhost:8080/health`
- **POST** `http://localhost:8080/items` con body JSON:
  ```json
  {"name": "primer-item"}
  ```
- **GET** `http://localhost:8080/items`

### 10. Probemos SoapUi y el web service SOAP

Debemos importar en SoapUi el proyecto ya definido en `labs/Lab01-2-soapui-project.xml`, y procedemos a ejecutar cada request.

**Nota: tambien podemos cargar el proyecto, asociando directamente la url del wsdl.** http://localhost:8080/soap?wsdl

- **echo:**
```XML
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:lab.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:echo>
         <!--Optional:-->
         <urn:s>test</urn:s>
      </urn:echo>
   </soapenv:Body>
</soapenv:Envelope>
```
- **create_item:**
```XML
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:lab.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:create_item>
         <!--Optional:-->
         <urn:name>soap-item-name</urn:name>
      </urn:create_item>
   </soapenv:Body>
</soapenv:Envelope>
```
- **list_items:**
```XML
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:lab.soap">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:list_items/>
   </soapenv:Body>
</soapenv:Envelope>
```

### 11. Probemos DBeaver y la base de datos PostgreSQL

Debemos abrir la aplicación DBeaver y crear una nueva conexión, posteriormente elegir el motor de base de daos (postgreSQL), y configurar los siguientes parametros:

- host: localhost
- puerto: 5432
- base de datos: labdb
- usuario: labuser
- contraseña: labpass

y al ser exitosa la conexión podremos visualizar la tabla de items, en nuestro esquema, y podremos tratar de agregar mas registros desde la base de datos.

