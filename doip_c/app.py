# coding: utf -8
import PySimpleGUI as sg # ライブラリの読み込み
import udp
import tcp

# テーマの設定
sg.theme("SystemDefault ")

# 事前設定
L1 = [
	# 診断機設定
	[sg.Text("・IPアドレス "),
	sg.InputText(default_text="127.0.0.1" , text_color = "#000000",background_color ="#ffffff",		size=(15,1),	key="-IP_EQP-" ),
	sg.Text("     ")],
	[sg.Text("・ポート番号 "),
	sg.InputText(default_text="13401" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(8,1),		key="-PORT_EQP-" )]]

	# ＧＷ設定
L2 = [
	[sg.Text("・IPアドレス "),
	sg.InputText(default_text="127.0.0.2" , text_color = "#000000",background_color ="#ffffff" ,	size=(15,1),	key="-IP_GW-" ),
	sg.Text("     ")],
	[sg.Text("・ポート番号 "),
	sg.InputText(default_text="13400" ,	text_color = "#000000",background_color ="#ffffff" ,		size=(8,1),		key="-PORT_GW-" )]]
L3 = [
	[sg.Multiline(default_text="", border_width=1,	size=(145,10),	key="-COM_ST-")]]

# UDP
L4 = [[sg.Button("送信", border_width=4 ,												size =(15,1),	key="-BTN_SEND_UDP-")],			# ボタン
	## Vehicle identification request message
	[sg.Radio(text='Vehicle identification request message',							size=(60,1) ,	key="-CMD_UDP_VIR-"	,	group_id='CMD_UDP') ],
	## Vehicle identification request message with EID
	[sg.Radio(text='Vehicle identification request message with EID',					size=(35,1) ,	key="-CMD_UDP_VIR_EID-" ,	group_id='CMD_UDP') ],
	[sg.Text("・EID", size=(10,1)) , sg.InputText(default_text="112233445566" ,			size=(23,1) ,	key="-TXT_ID-")],
	## Vehicle identification request message with VIN
	[sg.Radio(text='Vehicle identification request message with VIN',					size=(35,1) ,	key="-CMD_UDP_VIR_VIN-" ,	group_id='CMD_UDP')],
	[sg.Text("・VIN (ASCII)", size=(10,1)) , sg.InputText(default_text="0123456789ABCDEFF0" ,		size=(23,1) ,	key="-TXT_VIN-")],
	## DoIP entity status request
	[sg.Radio(text='DoIP entity status request',										size=(35,1) ,	key="-CMD_UDP_DISR-" ,	group_id='CMD_UDP')],
	## Diagnostic power mode information request
	[sg.Radio(text='Diagnostic power mode information request',							size=(35,1) ,	key="-CMD_UDP_DPMIR-" ,	group_id='CMD_UDP')],
	## UDP FREE Message
	[sg.Radio(text='FREE MESSAGE',														size=(15,1) ,	key="-CMD_UDP_FREE-"	,	group_id='CMD_UDP')],
	[sg.Multiline(default_text="" , border_width=2,										size=(63,8),	key="-TXT_UDP_FREE-")]]

# TCP
L5 = [[sg.Button("接続", border_width=4 , 												size =(15,1),	key="btn_connect_tcp"),				# ボタン
	sg.Button("切断", border_width=4 , 													size =(15,1),	key="btn_close_tcp"),				# ボタン
	sg.Button("送信", border_width=4 , 													size =(15,1),	key="btn_send_tcp")],				# ボタン
	## Routing activation request
	[sg.Radio(text='Routing activation request',										size=(60,1) ,	key="-CMD_TCP_RAR-"	,	group_id='CMD_TCP') ],
	[sg.Text("・SA", size=(10,1)) , sg.InputText(default_text="0E00" ,					size=(7,1) ,	key="-TXT_SA1-")],
	## Alive check request
	[sg.Radio(text='Alive check request',												size=(35,1) ,	key="-CMD_TCP_ACR-"	,	group_id='CMD_TCP') ],
	## Diagnostic message
	[sg.Radio(text='Diagnostic message',												size=(35,1) ,	key="-CMD_TCP_DM-"	,	group_id='CMD_TCP')],
	[sg.Text("・SA", size=(10,1)) , sg.InputText(default_text="0E00" ,					size=(7,1) ,	key="-TXT_SA2-"),
	sg.Text("・TA", size=(7,1)) , sg.InputText(default_text="0F00" ,					size=(7,1) ,	key="-TXT_TA-")],
	[sg.Text("・User data", size=(10,1)),sg.Multiline(default_text="", border_width=2,	size=(50,3),	key="-TXT_DIAG-")],
	## FREE Message
	[sg.Radio(text='FREE MESSAGE',														size=(15,1) ,	key="-CMD_TCP_FREE-"	,	group_id='CMD_TCP')],
	[sg.Multiline(default_text="" , border_width=2,										size=(63,8),	key="-TXT_TCP_FREE-")]]


L = [[sg.Frame("DoIPクライアント（診断機）",L1),sg.Frame("DoIPサーバ（ゲートウェイ）",L2)],
	[sg.Frame("UDP",L4),sg.Frame("TCP",L5)],
	[sg.Frame("通信ステータス",L3)]]

# ウィンドウ作成
window = sg.Window ("DoIP cliant tool", L)


def main():
	rtn = ""
	# イベントループ
	while True:
		# イベントの読み取り（イベント待ち）
		event , values = window.read()
		# 確認表示
		print(" イベント:",event ,", 値:",values)
		# print(bytearray.fromhex(values['-TXT_ID-']))
		# 終了条件（ None: クローズボタン）
		if event == "-BTN_SEND_UDP-":
			print("UDP送信")
			rtn = main_udp_send_cmd(values)
		# TCP接続
		elif event == "btn_connect_tcp":
			rtn = tcp.tcp_connect( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) )
		# TCP切断
		elif event == "btn_close_tcp":
			rtn = tcp.tcp_close()
		elif event == "btn_send_tcp":
			rtn = main_tcp_send_cmd(values)
		elif event == None:
			print(" 終了します． ")
			break
		window["-COM_ST-"].Update(rtn)
	# 終了処理
	window.close()


def main_udp_send_cmd(values):
	if values["-CMD_UDP_VIR-"] == True:
		data = "-CMD_UDP_VIR-"
	elif values["-CMD_UDP_VIR_EID-"] == True:
		data = "-CMD_UDP_VIR_EID-"
	elif values["-CMD_UDP_VIR_VIN-"] == True:
		data = "-CMD_UDP_VIR_VIN-"
	elif values["-CMD_UDP_DISR-"] == True:
		data = "-CMD_UDP_DISR-"
	elif values["-CMD_UDP_DPMIR-"] == True:
		data = "-CMD_UDP_DPMIR-"
	elif values["-CMD_UDP_FREE-"] == True:
		data = "-CMD_UDP_FREE-"
	else:
		data = "UDP送信エラー"
		return
	rtn = udp.udp_send( values['-IP_EQP-'] , values['-IP_GW-'] , int(values['-PORT_EQP-']) , int(values['-PORT_GW-']) , data )
	return data


def main_tcp_send_cmd(values):
	if values["-CMD_TCP_RAR-"] == True:
		data = "-CMD_TCP_RAR-"
	elif values["-CMD_TCP_ACR-"] == True:
		data = "-CMD_TCP_ACR-"
	elif values["-CMD_TCP_DM-"] == True:
		data = "-CMD_TCP_DM-"
	elif values["-CMD_TCP_FREE-"] == True:
		data = "-CMD_TCP_FREE-"
	else:
		data = "TCP送信エラー"
		return
	rtn = tcp.tcp_send( data )
	return data


main()