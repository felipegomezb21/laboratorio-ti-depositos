echo "[*] Validando correspondencia cert ↔ key por modulus"

S1=$(openssl x509 -noout -modulus -in certs/server.crt | openssl md5)
S2=$(openssl rsa  -noout -modulus -in certs/server.key | openssl md5)

if [[ "$S1" != "$S2" ]]; then
  echo "[!] server.crt y server.key NO corresponden"; exit 1
fi