from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from maincontroller import MainController 
import json

class LedControllerServer(BaseHTTPRequestHandler):

    controller = MainController()
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        print "in post method " + self.data_string

        self.send_response(200)
        self.end_headers()
        self.controller.changeMode(json.loads(self.data_string))
        self.wfile.write("Ok!")
        return

def run(server_class=HTTPServer, handler_class=LedControllerServer, port=2000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()