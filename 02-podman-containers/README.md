# Laboratorio 02 - Contenedores con Podman

**Objetivo:** Comprender de forma práctica cómo usar Podman (o Docker) para construir y ejecutar contenedores, explorando imágenes, volúmenes y herramientas de diagnóstico.

**Requerimientos:** Git, Podman 4.x (o Docker 24+), editor de texto y acceso a terminal.

**Duración estimada:** 45 minutos.

## Conceptos Clave

- **Imagen vs Contenedor:** La imagen es el artefacto inmutable; el contenedor es la instancia en ejecución basada en esa imagen.
- **Registro de Imágenes:** Repositorio (p. ej. Docker Hub, Quay.io) que aloja imágenes públicas o privadas.
- **Rootless Podman:** Podman puede ejecutar contenedores sin privilegios de root, reduciendo la superficie de ataque comparado con Docker tradicional.
- **Volúmenes:** Mecanismo para persistir datos fuera del ciclo de vida efímero del contenedor.
- **Logs / Exec / Inspect:** Comandos para diagnosticar, entrar y entender el estado actual de un contenedor.

## Agenda Sugerida (45 min)

- 5 min — Preparar entorno y repaso de comandos base.
- 10 min — Diferenciar imagen vs contenedor (pull, run, lifecycle).
- 10 min — Desplegar contenedor público y exponer servicio.
- 10 min — Construir imagen propia y correrla con volúmenes.
- 10 min — Trabajar con logs, exec, inspect y diferencias Podman vs Docker.

## Paso a Paso

### 1. Preparar el entorno

```bash
git clone git@github.com:nuamx/nmx-png-laboratorio-ti-depositos.git
cd nmx-png-laboratorio-ti-depositos/02-podman-containers
podman version   # o docker version
```

Si trabajas con Docker Desktop, todos los comandos `podman` tienen equivalente directo cambiando la palabra clave (`docker run`, `docker build`, etc.).

### 2. Imagen vs Contenedor (pull & lifecycle)

```bash
podman pull docker.io/library/nginx:alpine
podman images
podman run --name web-temp -d nginx:alpine
podman ps
podman stop web-temp
podman ps
podman ps --all
podman start web-temp
podman ps
podman stop web-temp
podman rm web-temp
podman ps --all
```

- Revisa `podman history nginx:alpine` para inspeccionar capas.
- Borra la imagen (`podman rmi nginx:alpine`) y verifica que desaparece de `podman images`.

### 3. Ejecutar un contenedor público y exponerlo

```bash
podman run --name lab-nginx -d -p 8080:80 nginx:alpine
curl http://localhost:8080
podman ps --filter name=lab-nginx
```

- Cambia el puerto interno (`-p 8081:80`) y verifica diferencias.
- Detén y elimina cuando termines:
  ```bash
  podman stop lab-nginx
  podman rm lab-nginx
  ```

### 4. Explorar contenedores (logs, exec, inspect)

Repite con un contenedor nuevo:

```bash
podman run --name inspectable -d -p 8080:80 nginx:alpine
podman logs inspectable
podman exec -it inspectable sh
podman inspect inspectable
podman inspect inspectable --format '{{ .NetworkSettings.IPAddress }}'
podman stats --no-stream
podman stats
```

Para Docker reemplaza `podman` por `docker`. Sal del shell con `exit`, luego detén el contenedor.

### 5. Construir tu propia imagen (Containerfile)

Revisa el `Containerfile` base en `services/app/Containerfile`, que construye una API FastAPI:

```bash
cat services/app/Containerfile
```

Compila la imagen:

```bash
podman build -t podman-notes:latest ./services/app
podman images | grep podman-notes
```

### 6. Correr la imagen con volúmenes y persistencia

La aplicación persiste notas en `/app/data/notes.json`. Crea un volumen y ejecuta el contenedor:

```bash
podman volume create notes-data
podman volume ls
podman run --name notes-api -d \
  -p 8090:8080 \
  -e NOTES_PATH=/app/data/notes.json \
  -v notes-data:/app/data \
  podman-notes:latest
```

Prueba la API:

```bash
curl http://localhost:8090/health
curl -X POST http://localhost:8090/notes -H "Content-Type: application/json" \
  -d '{"text":"mi primera nota"}'
curl http://localhost:8090/notes
```

Recrea el contenedor (`podman rm -f notes-api`) y vuélvelo a levantar; las notas permanecen porque residen en el volumen.

### 7. Diagnóstico: logs, exec e inspect sobre tu imagen

```bash
podman logs -f notes-api
podman exec -it notes-api ls /app/data
podman inspect notes-api | jq '.[0].Mounts'
```

Observa cómo el archivo `notes.json` existe dentro del volumen. Si no tienes `jq`, omite el pipe y revisa la salida manualmente.

### 8. Orquestar con Podman Compose

El archivo `compose.yaml` define la misma API y volumen:

```bash
cat compose.yaml
podman compose up --build
```

En otra terminal valida la API (`curl http://localhost:8085/notes`). Detén con `Ctrl+C` y libera recursos:

```bash
podman compose down
podman volume ls | grep notes
```

### 9. Diferencias rápidas Podman vs Docker (rootless)

- Podman puede ejecutar contenedores sin daemon y sin privilegios de root (`podman --remote` / user namespaces).
- Los comandos son compatibles: `alias docker=podman` es válido en la mayoría de escenarios.
- Podman usa `podman machine` en macOS/Windows para crear una VM rootless; Docker Desktop usa un daemon privilegiado.
- Los volúmenes rootless se almacenan en `$HOME/.local/share/containers/storage/volumes`.
- Para correr en CI o servidores sin sudo, Podman simplifica el hardening.

## Recursos adicionales

- Documentación oficial Podman: <https://podman.io/docs>
- FastAPI: <https://fastapi.tiangolo.com/>
- Diferencias Podman vs Docker: <https://podman.io/whatis>

Al finalizar, limpia artefactos si lo deseas:

```bash
podman rm -f notes-api inspectable || true
podman volume rm notes-data || true
podman rmi podman-notes:latest || true
```
