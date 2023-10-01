from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mimetypes
from pathlib import Path
import socket
from threading import Thread   
import urllib.parse

HTTP_PORT = 3000
SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 5000
STORAGE_PATH = Path("storage")
FRONTEND_PATH = Path("./front-init")

URL_TO_FILE_MAPPING = {
    '/': 'index.html',
    '/message': 'message.html',
}

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        file_path = URL_TO_FILE_MAPPING.get(pr_url.path)
        
        if file_path:
            self.send_response(200)
            self.send_file(file_path)
        else:
            self.send_response(404)
            self.send_file('error.html')

    def send_file(self, file_path):
        file_path = FRONTEND_PATH / file_path
        mt = mimetypes.guess_type(file_path)
        content_type = mt[0] if mt[0] else 'text/plain'
        
        self.send_header('Content-type', content_type)
        self.end_headers()
        
        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()



def save_data(data):
    data_parse = urllib.parse.unquote_plus(data.decode())

    data_path = STORAGE_PATH.joinpath("data.json")
    try:
        with open(data_path, encoding="utf-8") as file:
            data_json = json.load(file)
    except FileNotFoundError:
        data_json = {}
    data_json[str(datetime.now())] = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

    with open(data_path, "w", encoding="utf-8") as fh:
        json.dump(data_json, fh, indent=4, ensure_ascii=False)


def send_data_to_socket(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (SOCKET_IP, SOCKET_PORT))
    sock.close()


def run_socket_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            save_data(data)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


def run_http_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    print("Server started!")
    if not STORAGE_PATH.exists():
        STORAGE_PATH.mkdir()

    http_server_thread = Thread(target=run_http_server)
    http_server_thread.start()

    socket_server_thread = Thread(target=run_socket_server, args=(SOCKET_IP, SOCKET_PORT))
    socket_server_thread.start()

    http_server_thread.join()
    socket_server_thread.join()