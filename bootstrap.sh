#!/usr/bin/env bash

# Create keys and certificates
for dest in server client
do
	mkdir -p ${dest}
	openssl req -new -x509 -keyout ${dest}/${dest}-key.pem -out ${dest}/${dest}-cert.pem -days 14 -nodes -batch -subj "/CN=localhost" -verbose
done

# Copy certificates
cp server/server-cert.pem client
cp client/client-cert.pem server
