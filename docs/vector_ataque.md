# Vector de ataque

## Resumen

| Fase | Técnica | Objetivo |
|---|---|---|
| 1. Reconocimiento | Datos del silabo | Generar confianza |
| 2. Armamento | Landing + correo + payload | Preparar el engano |
| 3. Entrega | Correo de phishing | Que la victima haga clic |
| 4. Explotacion | Ejecucion como admin | Instalar keylogger |
| 5. Instalacion | Tarea programada | Persistencia |
| 6. C2 | POST HTTP cada 30s | Exfiltracion |
| 7. Acciones | Captura de teclas | Robo de credenciales |

## Infraestructura

Kali 192.168.56.10:
  - c2_server.py (puerto 8000)
  - phishing_server.py (puerto 8080)
  - landing/index.html
  - capturas/

Windows 192.168.56.20:
  - victim.py
  - metasploit.ico
  - dist/MetasploitFramework-latest.exe

## Fases

### Fase 1: Reconocimiento

Se recopilan datos reales del silabo:
- Codigo de curso: 1ACB0026-2620-16145
- Profesor: Gianpaul Jesus Custodio Chavarria
- Semana: 10
- Tema: Metasploit Framework

### Fase 2: Armamento

- Landing clonada del aula virtual
- Correo phishing con datos reales
- Payload camuflado como instalador de Metasploit

### Fase 3: Entrega

- Envio del correo a la victima
- Clic en el enlace
- Descarga del ejecutable
- Windows Defender avisa
- La victima pulsa "Conservar" (indicado en el disclaimer)

### Fase 4: Explotacion

- La victima ejecuta como administrador
- El payload se copia a AppData
- Crea tarea programada
- Anade exclusiones en Defender

### Fase 5: Instalacion

- Tarea programada onlogon
- Copia en AppData
- Exclusion de Defender
- Nombre msfconsole.exe

### Fase 6: C2

- Captura con pynput
- Buffer en memoria
- Volcado a disco cada 2 segundos
- POST al C2 cada 30 segundos
- Rotacion del archivo

### Fase 7: Acciones

- Captura de credenciales en Gmail, bancos, etc.
- Visualizacion en el C2

## Mitigaciones

| Fase | Mitigacion |
|---|---|
| Reconocimiento | No exponer datos del curso |
| Entrega | Verificar remitente real |
| Explotacion | No ejecutar adjuntos |
| Persistencia | Auditar tareas programadas |
| C2 | Firewall con inspeccion HTTP |
| Captura | EDR con proteccion de teclado, 2FA |
| Todo | Concienciacion del usuario |
