import time
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from paths import get_page_data, save_page

HOST_NAME = 'localhost'
PORT_NUMBER = 9000

# Only handles serving. Path parsing is done in the paths module.
# TODO: post

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self._set_headers(200, 'text/html')

    def do_POST(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type']
            }
        )

        if self.path == '/save_page':
            save_page(form)

        self._set_headers(200, 'text/html')

    def do_GET(self):
        self._respond('text/html')

    def _respond(self, content_type):
        page_data = get_page_data(self.path)
        self._set_headers(page_data['status'], content_type)
        response = bytes(page_data['content'], 'UTF-8')
        self.wfile.write(response)

    def _set_headers(self, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()


if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
