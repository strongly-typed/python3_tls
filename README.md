# Client-Server and Server-Client Authentication with Python3 TLS and Certificates

Let your client authenticate the server and your server your client.

## Introduction

When connecting to e.g. online banking it is standard that the client uses TLS to verify the authenticity of the banking server by certificates. The bank accepts connections from nearly any client. The client then uses credentials (username/PIN) to log in.

It is possible that the server only accepts a connection if the client presents a valid certificate to log in. That is a quite common procedure for passwordless SSH logins.

## Demo

    ./bootstrap.sh

Creates client and server ceritificates and distributes them accordingly. The private key always stays with the creator. The public certificate is provided to the communication partner.

|   Server     |  Client  |
|--------------|-------------|
| server-cert  | server-cert |
| server-key   |             |
| client-cert  | client-cert |
|              | client-key  |

The server is using latest TLSv1.2 configuration. Start it with

    cd server
    python3 webserver.py

In this demo `curl` is used as a client on OSX. It must be compiled with OpenSSL or libreSSL.

    brew remove curl
    brew install --with-openssl curl

The server is serving at port 4443 at localhost, so point curl to it:

	cd client
	/usr/local/opt/curl/bin/curl -tlsv1.2 -trace-time -4 --cacert server-cert.pem --key client-key.pem  --cert client-cert.pem -v -v https://localhost:4443

The expected result is

	* Rebuilt URL to: https://localhost:4443/
	*   Trying 127.0.0.1...
	* TCP_NODELAY set
	* Connected to localhost (127.0.0.1) port 4443 (#0)
	* ALPN, offering http/1.1
	* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
	* successfully set certificate verify locations:
	*   CAfile: server-cert.pem
	  CApath: none
	* TLSv1.2 (OUT), TLS header, Certificate Status (22):
	* TLSv1.2 (OUT), TLS handshake, Client hello (1):
	* TLSv1.2 (IN), TLS handshake, Server hello (2):
	* TLSv1.2 (IN), TLS handshake, Certificate (11):
	* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
	* TLSv1.2 (IN), TLS handshake, Request CERT (13):
	* TLSv1.2 (IN), TLS handshake, Server finished (14):
	* TLSv1.2 (OUT), TLS handshake, Certificate (11):
	* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
	* TLSv1.2 (OUT), TLS handshake, CERT verify (15):
	* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
	* TLSv1.2 (OUT), TLS handshake, Finished (20):
	* TLSv1.2 (IN), TLS change cipher, Client hello (1):
	* TLSv1.2 (IN), TLS handshake, Finished (20):
	* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
	* ALPN, server accepted to use http/1.1
	* Server certificate:
	*  subject: CN=localhost
	*  start date: Sep 13 21:39:07 2016 GMT
	*  expire date: Sep 27 21:39:07 2016 GMT
	*  common name: localhost (matched)
	*  issuer: CN=localhost
	*  SSL certificate verify ok.
	> GET / HTTP/1.1
	> Host: localhost:4443
	> User-Agent: curl/7.50.2
	> Accept: */*
	>
	* HTTP 1.0, assume close after body
	< HTTP/1.0 200 OK
	< Server: BaseHTTP/0.6 Python/3.5.2
	< Date: Tue, 13 Sep 2016 21:39:40 GMT
	< Content-type: text/html
	< Content-Length: 12
	<
	* Curl_http_done: called premature == 0
	* Closing connection 0
	* TLSv1.2 (OUT), TLS alert, Client hello (1):
	Hello world!%

The connection will fail when either the server or the client cannot provide its private key.

## ToDo

Ubuntu's 16.04 LTS curl complains if `Content-Length` is not set.

    * GnuTLS recv error (-110): The TLS connection was non-properly terminated.
    * Closing connection 0

[That is the reason](http://security.stackexchange.com/questions/82028/ssl-tls-is-a-server-always-required-to-respond-to-a-close-notify)