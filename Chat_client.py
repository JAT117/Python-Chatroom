#usage: python Chat_client.py

import socket, string, sys, select

#host = "192.168.1.105"
host = "127.0.0.1" #testing for local host
port = 9999

def prompt() :
	sys.stdout.write('<You> ')
	sys.stdout.flush()

if __name__ == "__main__":

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(2) #client drops after 2 seconds

	name = raw_input('Whats your name?: ')

	#attempt to connect to server
	try :
		s.connect((host, port))
	except :
		print 'Unable to connect'
		sys.exit()

	print 'Connected to remote host. Start sending messages'
	prompt()

	while True:
		socket_list = [sys.stdin, s]

		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

		for sock in read_sockets:
			 #incoming message from remote server
			if sock == s:
				data=sock.recv(2048)
				if not data:
					print '\nDisconnected from Server'
					sys.exit()
				else:
					#print data
					sys.stdout.write(data)
					prompt()

			 #user entered a message
			else:
				msg = name + ": " + sys.stdin.readline()
				s.send(msg)
				prompt()


