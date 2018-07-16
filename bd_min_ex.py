# Minimum working example of connecting PyBluez into Nengo

import numpy as np
import nengo
import bluetooth
import time

bd_port = 1
bd_size = 1024
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bd_port))
server_socket.listen(1)

client_socket, client_addr = server_socket.accept()
client_socket.setblocking(False)

print("Accepted connection with: " + str(client_addr))

last_data = 0.0
model = nengo.Network()
with model:

    def bd_recv(t):
        global last_data
        try:
            data = client_socket.recv(bd_size)
            data = -2 * float(data) + 1
            #print("tried")
            #print(data)
        except:
            data = last_data
            #print("excepted")
        time.sleep(0.001)

        last_data = data
        return data

    received = nengo.Node(bd_recv)

    # Create the neuronal ensembles
    a = nengo.Ensemble(n_neurons=100, dimensions=1)
    b = nengo.Ensemble(n_neurons=100, dimensions=1)

    # Connect the input to the first neuronal ensemble
    nengo.Connection(received, a)

    # Connect the first neuronal ensemble to the second using a
    # neurotransmitter with a 10ms time constant
    # This is the communication channel.
    nengo.Connection(a, b, synapse=0.01)

sim = nengo.Simulator(model)
sim.run(20, progress_bar=False)

client_socket.close()
server_socket.close()
