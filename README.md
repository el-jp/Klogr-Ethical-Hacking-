# Klogr-Ethical-Hacking-
Todo este material es exclusivamente para el laboratorio aislado del curso de Hacking Ético. No debe usarse contra sistemas, cuentas o personas reales. Al terminar la práctica, restaurar el snapshot o ejecutar los comandos de limpieza.

# Laboratorio de Phishing + Keylogger con bypass de Windows Defender

## Contexto

Laboratorio controlado para el curso de Hacking Ético. Todas las pruebas se
realizan en máquinas virtuales aisladas en red host-only. No se utiliza
contra sistemas reales ni cuentas ajenas.

## Requisitos

- 2 VMs: Kali Linux y Windows 10
- Red host-only (VMnet2 en VMware o red interna en VirtualBox)
- IPs:
  - Kali: 192.168.56.10
  - Windows: 192.168.56.20

## Estructura

kali/
    c2_server.py               Servidor C2 en puerto 8000
    phishing_server.py         Servidor web en puerto 8080
    landing/index.html         Landing clonada del aula virtual

windows/
    victim.py                  Codigo fuente del keylogger
    MetasploitFramework-latest.spec   Spec de PyInstaller
    metasploit.ico             Icono de Metasploit

email/
    anuncio_semana10.eml       Correo de phishing

docs/
    vector_ataque.md           Descripcion completa del vector
    asignacion_ip_kali.md      Como asignar IP a Kali
    limpieza.md                Como limpiar todo despues de la demo

## Flujo

1. Compilar victim.py en Windows con PyInstaller
2. Copiar el .exe a kali/landing/
3. Arrancar c2_server.py y phishing_server.py en Kali
4. Enviar anuncio_semana10.eml a la victima
5. La victima hace clic, descarga y ejecuta como admin
6. Los logs llegan al C2 en Kali

## Aviso

Solo para uso educativo en laboratorio aislado. El uso sin autorizacion
es delito.
