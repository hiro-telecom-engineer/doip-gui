# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
import udp
import tcp
import threading
import sys

# テーマの設定
sg.theme("SystemDefault ")

# 事前設定
L1 = [[sg.Text("・IPアドレス ",size=(18,1)),
	sg.InputText(default_text="127.0.0.2" , text_color = "#000000",background_color ="#ffffff" ,	size=(23,1),	key="-IP_GW" )],
	[sg.Text("・ポート番号 ",size=(18,1)),
	sg.InputText(default_text="13400" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(23,1),		key="-PORT_GW-" )],
	[sg.Text("・EID ",size=(18,1)),
	sg.InputText(default_text="112233445566" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(23,1),		key="-EID_GW-" )],
	[sg.Text("・VIN (ASCII) ",size=(18,1)),
	sg.InputText(default_text="0123456789ABCDEFF0" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(23,1),		key="-VIN_GW-" )],
	[sg.Text("・ロジカルアドレス ",size=(18,1)),
	sg.InputText(default_text="0001" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(23,1),		key="-LOGICAL_ADDRESS-" )]]
# UDP
L2 = [[sg.Button("OPEN", border_width=4 ,												size =(16,1),	key="-BTN_UDP_OPEN-")]]			# ボタン

# TCP
L3 = [[sg.Button("OPEN", border_width=4 , 												size =(16,1),	key="-BTN_TCP_OPEN-")]]				# ボタン

# 通信ステータス
L4 = [[sg.Multiline(default_text="", border_width=1,	size=(42,10),	key="-COM_ST-")]]

L = [[sg.Frame("DoIPサーバ設定",L1)],
	[sg.Frame("UDP",L2),sg.Frame("TCP",L3)],
	[sg.Frame("通信ステータス",L4)]]

# ウィンドウ作成
window = sg.Window ("DoIP sever tool", L)

if __name__ == '__main__':
	threads = []
	# イベントループ
	while True:
		# イベントの読み取り（イベント待ち）
		event , values = window.read()
		# 確認表示
		print(" イベント:",event ,", 値:",values)
		# 終了条件（ None: クローズボタン）
		if event == "-BTN_UDP_OPEN-":
			t1 = threading.Thread(target=udp.udp_recv, args=(values['-IP_GW'] , int(values['-PORT_GW-']),))
			threads.append(t1)
			t1.setDaemon(True)
			t1.start()
			print("UDP OPEN")
		# TCP接続
		elif event == "-BTN_TCP_OPEN-":
			t2 = threading.Thread(target=tcp.tcp_recv, args=(values['-IP_GW'] , int(values['-PORT_GW-']),))
			threads.append(t2)
			t2.setDaemon(True)
			t2.start()
			print("TCP OPEN")
		elif event == None:
			sys.exit()


