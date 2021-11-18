# Usage: python simpleserver.py PORT USERNAME:PASSWORD
from http.server import SimpleHTTPRequestHandler
import socketserver
import sys, base64

key = ""

class AuthHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_GET(self):
        global key

        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received'.encode())
        elif self.headers.get('Authorization') == 'Basic ' + key.decode():
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get('Authorization').encode())
            self.wfile.write('not authenticated'.encode())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage BasicAuthServer.py [port] [username:password]")
        sys.exit()

    PORT = int(sys.argv[1])
    key = base64.b64encode(sys.argv[2].encode())
    with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
