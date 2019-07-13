import socket
from views import *


class WebApplication:
    def __init__(self, host='127.0.0.1', port=5000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.urls = {
            '/': index,
            '/blog': blog    
        }

    def parse_request(self, request):
        parsed = request.split(' ')
        method = parsed[0]
        url = parsed[1]
        return (method, url)

    def generate_headers(self, method, url):
        if not method == 'GET':
            return ('HTTP/1.1 405 Method not allowed\n\n', 405)
        elif not url in self.urls:
            return ('HTTP/1.1 404 Not found\n\n', 404)
        return ('HTTP/1.1 200 OK\n\n', 200)

    def generate_content(self, code, url):
        if code == 404:
            return '<h1>404</h1><p>Not found</p>'
        elif code == 405:
            return '<h1>405</h1><p>Not allowed method</p>'
        return self.urls[url]()

    def generate_response(self, request):
        method, url = self.parse_request(request)
        headers, code = self.generate_headers(method, url)
        body = self.generate_content(code, url)
        return (headers + body).encode()

    def run(self):
        while True:
            client, addr = self.server.accept()
            request = client.recv(1024)

            response = self.generate_response(request.decode())
            client.sendall(response)
            client.close()


if __name__ == '__main__':
    app = WebApplication()
    app.run()
