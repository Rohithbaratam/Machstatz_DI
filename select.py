'''Python’s select() function is a direct interface to the underlying operating system implementation. 
It monitors sockets, open files, and pipes (anything with a fileno() method that returns a valid file descriptor) until they become readable or writable or a communication error occurs. 
select() makes it easier to monitor multiple connections at the same time, and is more efficient than writing a polling loop in Python using socket timeouts, 
because the monitoring happens in the operating system network layer, instead of the interpreter.
'''


import select
import socket
import sys
import queue

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address),
      file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections
server.listen(5)

'''
The arguments to select() are three lists containing communication channels to monitor. 
The first is a list of the objects to be checked for incoming data to be read, the second contains objects that will receive outgoing data when there is room in their buffer, 
and the third those that may have an error (usually a combination of the input and output channel objects). 
'''

