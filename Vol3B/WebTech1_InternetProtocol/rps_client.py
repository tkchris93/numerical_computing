# rps_client.py
"""Vol 3B: Web Tech 1 (Internet Protocols). Solutions file."""

import socket
from random import randint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10001)
sock.connect(server_address)

moves = ['rock', 'paper', 'scissors']
sock.sendall(moves[randint(0,2)])

while True:
    data = sock.recv(16)
    if data == 'You win!':
        print 'I won!'
        break
    else:
        sock.sendall(moves[randint(0,2)])

sock.close()
