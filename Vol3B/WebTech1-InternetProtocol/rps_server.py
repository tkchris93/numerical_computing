import socket, random

moves = ['rock','paper','scissors']

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10001)
print 'Starting up on: ',server_address

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)
keep_playing = True
inner = True

while keep_playing:
	print 'Waiting for a connection.'
	connection, client_address = sock.accept()
	
	try:
		print 'Connection from: ',client_address
		
		while inner:
			data = connection.recv(16)
			
			if data:
				print 'Received ',data
				
				if data in moves:
					mymoveindex = random.randint(0,2)
					mymove = moves[mymoveindex]
					yourmoveindex = moves.index(data)
					print data,' vs ',mymove
					
					if yourmoveindex == ((mymoveindex + 1) % 3):
						print 'Sending congratulations.'
						connection.sendall('You win!')
						keep_playing = False
						inner = False
					elif yourmoveindex == ((mymoveindex - 1) % 3):
						print 'Gloating!'
						connection.sendall('You lose!')
					else:
						print 'Losing patience.'
						connection.sendall('Draw!')
				else:
					print 'Criticizing poor decision.'
					connection.sendall('Invalid move.')
				
			else:
				print 'No more data from: ',client_address
				break
            
	finally:
		connection.close()
