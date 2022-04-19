from socket import socket, AF_INET, SOCK_STREAM


def tcp_connect( src_ip , dst_ip , src_port , dst_port ):
	global tcpClntSock
	# ソケット作成
	tcpClntSock = socket(AF_INET, SOCK_STREAM)
	tcpClntSock.settimeout(0.5)
	# 送信側アドレスをtupleに格納
	SrcAddr = ( src_ip , src_port )
	# 送信側アドレスでソケットを設定
	tcpClntSock.bind(SrcAddr)
	# サーバーに接続
	tcpClntSock.connect((dst_ip, dst_port))


def tcp_send( data ):
	global tcpClntSock
	try:
		tcpClntSock.send(data.encode('utf-8'))
		response = tcpClntSock.recv(4096)
		print(response)
	except ConnectionResetError:
		# ソケットクローズ
		tcpClntSock.close()
		return


def tcp_close():
	global tcpClntSock
	# ソケットクローズ
	tcpClntSock.close()
	print("TCP切断",tcpClntSock)


if __name__ == '__main__':
	tcp_connect( "127.0.0.1" , "127.0.0.1" , 13402 , 50000 )
	tcp_send( "Hello"  )
	tcp_close()
