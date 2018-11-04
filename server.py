import time
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from paths import get_response_data, save_page

HOST_NAME = 'localhost'
PORT_NUMBER = 9000

# Only handles serving. Path parsing is done in the paths module.
# TODO Cookies to remember what db the user is looking at

class RequestHandler(BaseHTTPRequestHandler):
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

    def _respond(self, content_type, cookie=None):
        data = get_response_data(self.path)
        self._set_headers(data['status'], content_type, cookie)
        response = bytes(data['content'], 'UTF-8')
        self.wfile.write(response)

    def _set_headers(self, status=200, content_type='text/html', cookie=None):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        if cookie:
            self.send_header('Set-Cookie', 'campaigndexdb={}'.format(cookie))
        self.end_headers()


if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), RequestHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
