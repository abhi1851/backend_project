# Certificates

Generate self-signed certificates for local TLS testing.

Usage:
  ./generate-certs.sh

This creates:
- ca.key, ca.crt (Certificate Authority)
- server.key, server.crt (server cert for host `kafka` and 127.0.0.1)

Point Kafka and clients to these PEM files. See docker-compose.secure.override.yml.
