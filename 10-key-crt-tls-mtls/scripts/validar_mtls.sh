#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f certs/server.crt ]]; then
  echo "[!] Ejecuta: la generación de certs"
  exit 1
fi

echo "[*] Conectando con cert de cliente (mtls)"

openssl s_client -connect 127.0.0.1:9443 -servername localhost \
  -cert certs/client.crt -key certs/client.key -CAfile certs/ca.crt -state -tlsextdebug </dev/null | head -n 60

