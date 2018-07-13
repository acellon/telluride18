# Communication Channel

# This example demonstrates how to create a connections from one neuronal
# ensemble to another that behaves like a communication channel (that is, it
# transmits information without changing it).

import numpy as np
import nengo
import bluetooth

bd_port = 1
bd_size = 1024
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bd_port))
server_socket.listen(1)

client_socket, client_addr = server_socket.accept()
print("Accepted connection with: " + str(client_addr))

model = nengo.Network()
with model:
    # Create an abstract input signal that oscillates as sin(t)
    def bd_recv(t):
        data = client_socket.recv(bd_size)
        data = -2 * float(data) + 1
        print(data)
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
sim.run(0.2)

client_socket.close()
server_socket.close()


