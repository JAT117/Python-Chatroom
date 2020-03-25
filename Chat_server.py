"""
usage: python Chat_server.py
"""
import socket, select, sys

# List of socket descriptors
CONNECTION_LIST = []
host = '127.0.0.1'
#host = '192.168.1.105'
RECV_BUFFER = 2048
port = 9999

def broadcast_data (sock, message):
	for socket in CONNECTION_LIST:
		if socket != server and socket != sock :
			try :
				socket.send(message)
			except :
				socket.close()
				CONNECTION_LIST.remove(socket)
				
def main():
	#create a TCP socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#socket options to reuse address or port when reconnection
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	#bind socket to host address and port
	server.bind((host, port))

	#Finally, listen for incomming connections 
	server.listen(100)

	# Add server socket to the list of readable connections
	CONNECTION_LIST.append(server)
	print "Chat server started on port " + str(port)

	while True:
		# Get the list sockets which are ready to be read through select
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

		for sock in read_sockets:
			#New connection
			if sock == server:

				sockfd, addr = server.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr

				broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
				
			else:
				# IF data was received from client, broadcast it to all others
				try:
					data = sock.recv(RECV_BUFFER)
					if data:
						broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)

				except:
					broadcast_data(sock, "Client (%s, %s) is offline" %addr)
					print "Client (%s, %s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue

	server.close()
	
if __name__ == "__main__":
	main()




