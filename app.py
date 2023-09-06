from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import pathlib
BASE_DIR = pathlib.Path()


class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(urllib.parse.urlparse(self.path))
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/contact':
            self.send_html_file('contact.html')
        else:
            self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


def run(server_class=HTTPServer, handler_class=MyHttpHandler):
    server_address = ('', 3000)
    http_server = server_class(server_address, handler_class)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__ == '__main__':
    run()
