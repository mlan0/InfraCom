import sys
import itertools
import socket
import os
import subprocess
from socket import socket as Socket

map = {}

def main():
    
    dnsSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    dnsSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Comunicacao com o server
    ############################

    dnsSocket.bind(('', 2010))
    dnsSocket.listen(1)

    print('------------Conectou com o SERVER')

    connection_socket = dnsSocket.accept()[0]

    print('Aceitou conexão com o SERVER')
    msg = connection_socket.recv(1024).decode('ascii')
    domainName, ipAddress = msg.split("#")
    print('Recebi do SERVER o dominio: ' + domainName)
    print('Recebi do SERVER o IP: ' + ipAddress)

    map[domainName] = ipAddress

    connection_socket.send('Mensagem do DNS para o SERVER'.encode('ascii'))

    ############################


    # Comunicacao com o Client
    ############################
    
    dnsClientSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    dnsClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    dnsClientSocket.bind(('', 2080))
    dnsClientSocket.listen(1)
    connection_socket = dnsClientSocket.accept()[0]

    print('------------Conectou com o CLIENT')

    while True:
        domainName = connection_socket.recv(1024).decode('ascii')
        print('Recebi do CLIENT o dominio ' + domainName)
        if not domainName:
            break
        if (domainName in map):
            msg = map.get(domainName)
            print('Enviando para CLIENT o IP: ' + ipAddress)
            connection_socket.send(ipAddress.encode('ascii'))
        else:
            msg = 'Nao existe esse dominio'
            print(msg)
            connection_socket.send(msg.encode('ascii'))


    #connection_socket.close()

    ############################
    
if __name__ == "__main__":
    sys.exit(main())