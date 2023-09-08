from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import pathlib
import mimetypes

import json

BASE_DIR = pathlib.Path()


class HTTPHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # self.send_html_file('message.html')
        body = self.rfile.read(int(self.headers['Content-Length']))
        body = urllib.parse.unquote_plus(body.decode())
        payload = {key: value for key, value in [
            el.split('=') for el in body.split('&')]}
        with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding='utf-8') as fd:
            json.dump(payload, fd, ensure_ascii=False)
        print(payload)

        self.send_response(302)
        self.send_header('Location', 'index.html')
        self.end_headers()

    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case'/':
                self.send_html_file('index.html')
            case'#message':
                self.send_html_file('message.html')
            case'#blog':
                self.send_html_file('blog.html')
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)

                else:
                    self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type = mimetypes.guess_type(filename)
        self.send_header('Content-type', mime_type)
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename):
        self.send_response(200)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-type', mime_type)
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


def run(server_class=HTTPServer, handler_class=HTTPHandler):
    server_address = ('', 3000)
    http_server = server_class(server_address, handler_class)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == '__main__':
    run()
