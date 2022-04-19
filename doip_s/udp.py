from socket import socket, AF_INET, SOCK_DGRAM
import time

def udp_recv( ip_addr , port ):
	# 受信側アドレスをtupleに格納
	SrcAddr = ( ip_addr , port)
	# バッファサイズ指定
	BUFSIZE = 1024
	# ソケット作成
	udpServSock = socket(AF_INET, SOCK_DGRAM)
	# 受信側アドレスでソケットを設定
	udpServSock.bind(SrcAddr)
	time.sleep(1)
	# While文を使用して常に受信待ちのループを実行
	while True:
		time.sleep(1)
		# ソケットにデータを受信した場合の処理
		# 受信データを変数に設定
		data, addr = udpServSock.recvfrom(BUFSIZE)
		# 受信データと送信アドレスを出力
		print(data.decode(), addr)
		udpServSock.sendto(data,addr)
