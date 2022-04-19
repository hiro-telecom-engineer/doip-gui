import socket
import time

BUFFER_SIZE = 1024

def tcp_recv( ip_addr , port ):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(( ip_addr , port))
		s.listen()

		time.sleep(1)
		while True:
			(connection, client) = s.accept()
			while True:
				try:
					print('Client connected', client)
					data = connection.recv(BUFFER_SIZE)
					print(data)
					connection.send("responce".encode('utf-8'))
				finally:
					print('close', client)


if __name__ == '__main__':
	tcp_recv( "127.0.0.1" , 50000 )