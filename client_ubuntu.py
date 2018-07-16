# Bluetooth client to connect to Surface Pro running Ubuntu

import bluetooth

bd_addr = "B4:AE:2B:E2:72:A5"

port = 2

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()
