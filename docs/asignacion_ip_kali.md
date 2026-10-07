# Asignacion de IP a Kali

## Opcion 1: Comando rapido (no persistente)

sudo ip addr flush dev eth0
sudo ip addr add 192.168.56.10/24 dev eth0
sudo ip link set eth0 up

Verificar:

ip a | grep 192.168.56

Debe mostrar:

inet 192.168.56.10/24 scope global eth0

Probar conectividad:

ping -c 2 192.168.56.20

## Si eth0 no existe

Comprobar el nombre real:

ip link show

Sustituir eth0 por el nombre real (ens33, enp0s3, etc.)

## Opcion 2: IP persistente con NetworkManager

Ver el nombre de la conexion:

nmcli connection show

Modificar:

sudo nmcli connection modify "Wired connection 1" ipv4.addresses 192.168.56.10/24 ipv4.method manual

Reiniciar:

sudo nmcli connection down "Wired connection 1"
sudo nmcli connection up "Wired connection 1"

Verificar:

ip a | grep 192.168.56

## Opcion 3: Editar archivo de NetworkManager

sudo nano /etc/NetworkManager/system-connections/"Wired connection 1".nmconnection

Seccion [ipv4]:

[ipv4]
method=manual
address1=192.168.56.10/24
dns-search=
may-fail=false

Reiniciar:

sudo systemctl restart NetworkManager

## Verificacion final

ip a | grep 192.168.56
ping -c 2 192.168.56.20
ip route

Debe mostrar:

192.168.56.0/24 dev eth0 proto kernel scope link src 192.168.56.10
