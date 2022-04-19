from socket import socket, AF_INET, SOCK_DGRAM

def udp_send( src_ip , dst_ip , src_port , dst_port , data ):
	# 送信側アドレスをtupleに格納
	SrcAddr = ( src_ip , src_port )
	# 受信側アドレスをtupleに格納
	DstAddr = ( dst_ip , dst_port )
	# ソケット作成
	udpClntSock = socket(AF_INET, SOCK_DGRAM)
	# 送信側アドレスでソケットを設定
	udpClntSock.bind(SrcAddr)
	# バイナリに変換
	data = data.encode('utf-8')
	# 受信側アドレスに送信
	udpClntSock.sendto(data,DstAddr)
	# バッファサイズ指定
	BUFSIZE = 1024

	# While文を使用して常に受信待ちのループを実行
	while True:
		# ソケットにデータを受信した場合の処理
		# 受信データを変数に設定
		data, addr = udpClntSock.recvfrom(BUFSIZE)
		# 受信データと送信アドレスを出力
		print(data.decode(), addr)
		break

# udp_send( "127.0.0.1" , "127.0.0.1" , 13401 , 13400 , "0000" )