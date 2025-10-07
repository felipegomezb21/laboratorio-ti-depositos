#!/usr/bin/env bash
set -euo pipefail

#Validación de que los certificados ya esten creados
if [[ ! -f certs/server.crt ]]; then
  echo "[!] Ejecuta: la generación de certs"
  exit 1
fi

echo "[*] Probando TLS hacia Nginx (requiere docker compose up)"

openssl s_client -connect 127.0.0.1:8443 -servername localhost -showcerts </dev/null | head -n 30 || true

