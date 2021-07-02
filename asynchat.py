#The asynchat module builds on asyncore to make it easier to implement protocols based on passing messages back and forth between server and client. 
#The async_chat class is an asyncore.dispatcher subclass that receives data and looks for a message terminator. 
#Your subclass only needs to specify what to do when data comes in and how to respond once the terminator is found. 
#Outgoing data is queued for transmission via FIFO objects managed by async_chat.


#The EchoServer example below uses both a simple string terminator and a message length terminator, depending on the context of the incoming data. 
#The HTTP request handler example in the standard library documentation offers another example of how to change the terminator based on the context to differentiate between HTTP headers and the HTTP POST request body.

import asyncore
import logging
import socket

from asynchat_echo_handler import EchoHandler

class EchoServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(1)
        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        EchoHandler(sock=client_info[0])
        # We only want to deal with one client at a time,
        # so close as soon as we set up the handler.
        # Normally you would not do this and the server
        # would run forever or until it received instructions
        # to stop.
        self.handle_close()
        return
    
    def handle_close(self):
        self.close()

        
        
#Client
#The client works in much the same way as the handler. As with the asyncore implementation, the message to be sent is an argument to the client’s constructor.
#When the socket connection is established, handle_connect() is called so the client can send the command and message data.


import asynchat
import logging
import socket


class EchoClient(asynchat.async_chat):
   
    ac_in_buffer_size = 64
    ac_out_buffer_size = 64
    
    def __init__(self, host, port, message):
        self.message = message
        self.received_data = []
        self.logger = logging.getLogger('EchoClient')
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s', (host, port))
        self.connect((host, port))
        return
        
    def handle_connect(self):
        self.logger.debug('handle_connect()')
        # Send the command
        self.push('ECHO %d\n' % len(self.message))
        # Send the data
        self.push_with_producer(EchoProducer(self.message, buffer_size=self.ac_out_buffer_size))
        # We expect the data to come back as-is, 
        # so set a length-based terminator
        self.set_terminator(len(self.message))
    
    def collect_incoming_data(self, data):
        """Read an incoming message from the client and put it into our outgoing queue."""
        self.logger.debug('collect_incoming_data() -> (%d)\n"""%s"""', len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            self.logger.debug('RECEIVED COPY OF MESSAGE')
        else:
            self.logger.debug('ERROR IN TRANSMISSION')
            self.logger.debug('EXPECTED "%s"', self.message)
            self.logger.debug('RECEIVED "%s"', received_message)
        return

class EchoProducer(asynchat.simple_producer):

    logger = logging.getLogger('EchoProducer')

    def more(self):
        response = asynchat.simple_producer.more(self)
        self.logger.debug('more() -> (%s bytes)\n"""%s"""', len(response), response)
        return response
