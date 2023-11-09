# server.py
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/confidential-file':
            # Check if the "isAdmin" cookie is present and set to true
            isAdmin_cookie = self.headers.get('Cookie', '')
            if 'isAdmin=true' in isAdmin_cookie:
                # Serve the confidential file
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                # Read and send the content of the confidential file
                with open(os.path.join('public', 'confidential.txt'), 'rb') as file:
                    self.wfile.write(file.read())
            else:
                # If the "isAdmin" cookie is not present or set to false, send a 403 Forbidden response
                self.send_response(403)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Access forbidden')
        else:
            # Serve other files using the default handler
            super().do_GET()

PORT = 8000

with HTTPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
