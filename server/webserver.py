#!/usr/bin/env python3

# /usr/local/opt/curl/bin/curl -tlsv1.2 -trace-time -4 -v -v \
#		--cacert server-cert.pem --key client-privatekey.pem \
#       --cert   client-cert.pem                             \
#       https://localhost:4443


from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

class myHandler(BaseHTTPRequestHandler):

	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		print('Get')
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Content-Length', '12')
		self.end_headers()
		self.wfile.write(b'Hello world!')
		self.wfile.flush()

# Setup server
# replace 'localhost' with '' to serve all hosts.
httpd = HTTPServer(('localhost', 4443), myHandler)

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
ssl_context.options = ssl.PROTOCOL_TLSv1_2
ssl_context.set_alpn_protocols(['http/1.1'])
ssl_context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')

# Use this private key to authenticate the server against the client
ssl_context.load_cert_chain(certfile='server-cert.pem', keyfile='server-key.pem')

# Expect that the client has the private key corresponding to that certificate
ssl_context.load_verify_locations(cafile='client-cert.pem')
ssl_context.verify_mode = ssl.CERT_REQUIRED

httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

httpd.serve_forever()
