# Bluetooth client to connect to Guido's AIY

import bluetooth

bd_addr = "B8:27:EB:72:31:96"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello!!")

sock.close()
