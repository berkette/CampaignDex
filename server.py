import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from paths import getPageData

HOST_NAME = 'localhost'
PORT_NUMBER = 9000

# Only handles serving. Path parsing is done in the paths module.
# TODO: post

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        return

    def do_GET(self):
        self.respond('text/html')

    def handle_http(self, content_type):
        page_data = getPageData(self.path)

        self.send_response(page_data['status'])
        self.send_header('Content-type', content_type)
        self.end_headers()
        return bytes(page_data['content'], 'UTF-8')

    def respond(self, content_type):
        response = self.handle_http(content_type)
        self.wfile.write(response)

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
