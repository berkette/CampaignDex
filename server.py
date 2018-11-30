import sys
import threading
import time
from http.server import HTTPServer
from settings import HOST_NAME, PORT_NUMBER, LOG_DIR, ROOT_DIR
from server import RequestHandler

class ServerThread(threading.Thread):
    def __init__(self, httpd):
        super().__init__()
        self.daemon = True
        self.httpd = httpd

    def run(self):
        with open(ROOT_DIR + LOG_DIR + "current_run.log", "w") as logfile:
            sys.stderr = logfile
            print(time.asctime(), 'Starting Server - %s:%s' % (HOST_NAME, PORT_NUMBER), file=sys.stderr)
            try:
                self.httpd.serve_forever()
            except Exception as e:
                traceback.print_exc()
            finally:
                self.httpd.server_close()
                print(time.asctime(), 'Server Stopped - %s:%s' % (HOST_NAME, PORT_NUMBER), file=sys.stderr)

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), RequestHandler)

    server_thread = ServerThread(httpd)
    server_thread.start()

    reply = input("Type something to exit... ")

    server_thread.httpd.shutdown()
    server_thread.join()
