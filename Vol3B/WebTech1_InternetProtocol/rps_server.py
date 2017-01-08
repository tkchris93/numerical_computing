# rps_server.py
"""Vol 3B: Web Tech 1 (Internet Protocols). Solutions file."""

import socket
from random import randint

# Global variables
moves = ['rock','paper','scissors']
server_address = ("localhost", 10001)
keep_playing = True
inner = True

# Start up the server.
print "Starting up on: {}".format(server_address)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)


while keep_playing:
	print "Waiting for a connection..."
	connection, client_address = sock.accept()

	try:
		print "Connection from: {}".format(client_address)

		while inner:
			data = connection.recv(16)

			if data:
				print "Received {}".format(data)

				if data in moves:
					my_move_index = randint(0,2)
					my_move = moves[my_move_index]
					your_move = moves.index(data)
					print "{} vs {}".format(data, my_move)

					if your_move == (my_move_index + 1) % 3: 		# Win
						# print "Sending congratulations."
						connection.sendall('You win!')
						keep_playing = False
						inner = False
					elif your_move == (my_move_index - 1) % 3: 	# Lose
						# print "Gloating!"
						connection.sendall('You lose!')
					else: 											# Draw
						# print "Losing patience."
						connection.sendall('Draw!')
				else:
					# print "Criticizing poor decision."
					connection.sendall("Invalid move.")

			else:
				print "No more data from: {}".format(client_address)
				break

	finally:
		connection.close()
