#!/usr/bin/env bash
cd Server/ssl
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 10000
