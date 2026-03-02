#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PASS=changeit
CN=kafka
keytool -genkeypair -alias $CN -keyalg RSA -keystore kafka.keystore.jks -storepass $PASS -keypass $PASS -dname "CN=$CN, OU=Dev, O=Acme, L=Berlin, S=BE, C=DE" -validity 3650
keytool -export -alias $CN -file kafka.cer -keystore kafka.keystore.jks -storepass $PASS
keytool -import -noprompt -alias $CN -file kafka.cer -keystore kafka.truststore.jks -storepass $PASS
cp kafka.truststore.jks client.truststore.jks
echo "Generated keystore + truststores (password: $PASS)"