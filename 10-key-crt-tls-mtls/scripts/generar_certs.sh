#!/usr/bin/env bash
set -euo pipefail #Detiene el script, en caso que alguna ejecución genere error.
mkdir -p certs

echo "[*] Generando CA (solo para laboratorio)"

################ CA Local

# Llave privada CA
openssl genrsa -out certs/ca.key 4096 >/dev/null 2>&1 

# Certificado CA
openssl req -x509 -new -nodes -key certs/ca.key -sha256 -days 3650 \
  -subj "/C=CO/ST=Antioquia/L=Medellin/O=Demo/OU=IT/CN=Demo-Root-CA" \
  -out certs/ca.crt

echo "[*] Generando llave y CSR de servidor (SAN=localhost,127.0.0.1)"

################ Servidor

# Llave privada servidor.
openssl genrsa -out certs/server.key 2048 >/dev/null 2>&1 

# Generación CSR del servidor.
openssl req -new -key certs/server.key -out certs/server.csr -config openssl/server.cnf 

echo "[*] Firmando certificado de servidor con la CA"

#Certificado firmado por el CA, desde el CSR del servidor.
openssl x509 -req -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
-out certs/server.crt -days 825 -sha256 -extensions v3_req -extfile openssl/server.cnf

################# Cliente

echo "[*] Generando llave y CSR de cliente"

# Llave privada clientes.
openssl genrsa -out certs/client.key 2048 >/dev/null 2>&1

# Generación CSR del cliente.
openssl req -new -key certs/client.key -subj "/C=CO/O=Demo/OU=IT/CN=demo-client" -out certs/client.csr

echo "[*] Firmando certificado de cliente con la CA"

#Certificado firmado por el CA, desde el CSR del cliente.
openssl x509 -req -in certs/client.csr -CA certs/ca.crt -CAkey certs/ca.key -CAserial certs/ca.srl \
  -out certs/client.crt -days 825 -sha256

echo "[+] Certificado y llave de servidor corresponden"

################ Paquetes de certificados y llaves, para cada necesidad.

echo "[*] Creando fullchain (server + CA) para Nginx"
### Cadena completa, requerida para la configuración TLS de Nginx
cat certs/server.crt certs/ca.crt > certs/fullchain.crt

echo "[*] Creando bundle PEM (server key crt + CA) para HAproxy"
### Formato requerido por HAproxy su TLS.
cat certs/server.key certs/server.crt certs/ca.crt > certs/bundle.pem

echo "[*] Creando pkcs12 p12 para el navegador, con fin de comprobar el mTLS "
openssl pkcs12 -export \
  -in certs/client.crt \
  -inkey certs/client.key \
  -out certs/client.p12 \
  -name "Certificado Cliente Demo" \
  -CAfile certs/ca.crt -caname root -password pass:1234

echo "[*] Listado de archivos en certs/: "
ls -1 certs | sed 's/^/  - /'
