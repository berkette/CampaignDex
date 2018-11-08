import time
import cgi
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from paths import get_response_data, post_action
from settings import HOST_NAME, PORT_NUMBER
from settings import STATUS_OK, STATUS_REDIRECT

# Only handles serving. Path parsing is done in the paths module.
# TODO Cookies to remember what db the user is looking at

class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self._set_headers(STATUS_OK, 'text/html')

    def do_GET(self):
        (parsed_path, get_vars) = self._parse_url()
        cookie = self._build_cookie()
        data = get_response_data(
            parsed_path,
            cookie=cookie,
            get_vars=get_vars
        )

        if data['status'] == STATUS_REDIRECT:
            self._set_headers(
                STATUS_REDIRECT,
                redirect_path = data['content'],
                set_cookie = data['set_cookie']
            )

        else:
            self._set_headers(
                data['status'],
                data['content_type'],
                content_length = data['content_length'])
            response = bytes(data['content'], 'UTF-8')
            self.wfile.write(response)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type']
            }
        )
        cookie = self._build_cookie()

        (redirect_path, set_cookie) = post_action(
            self.path,
            form,
            cookie=cookie
        )

        self._set_headers(
            STATUS_REDIRECT,
            redirect_path=redirect_path,
            set_cookie=set_cookie
        )

    ### Private Methods

    def _build_cookie(self):
        cookie_str = self.headers['Cookie']
        if cookie_str:
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
        else:
            cookie = None
        return cookie

    def _parse_url(self):
        # Used to get GET vars
        parsed = urlparse(self.path)
        get_vars = parse_qs(parsed.query)
        return (parsed.path, get_vars)

    def _set_headers(self, status=STATUS_OK, content_type='text/html',\
        content_length=None, set_cookie=[], redirect_path=None):
        if status == STATUS_REDIRECT and not redirect_path:
            raise Exception('Must specify redirect_path')

        self.send_response(status)
        self.send_header('Content-type', content_type)

#        if content_length:
#            self.send_header('Content-length', content_length)

        for cookie in set_cookie:
            self.send_header(
                'Set-Cookie',
                cookie[0] + '=' + cookie[1]
            )

        if redirect_path:
            self.send_header('Location', redirect_path)

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
