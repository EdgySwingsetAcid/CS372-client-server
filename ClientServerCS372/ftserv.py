import sys
import socket

class ftserv:
    """
    Class which represents the ftserv server.

    Contains routines to initialize components and listen for clients,
    receive data, validate commands sent from clients, and send data
    to clients over a TCP data connection.

    Author: Phillip Carter
    Class: CS 372, Winter 2014
    Last Modified: 2/17/2014
    """

    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024

    def __init__(self, host):
        """
        Initialization routine.
        1. Initializing components to listen on a TCP control connection.
        2. Initializing component which continuously waits on input from a client
        """

        print 'Connecting over host A on port 30021...'

        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen.bind((host, self.CTRLPORT))
        self.listen.listen(1)

        print 'Waiting on a client...'

    def start(self):
        """
        Routine which handles the following:
        
        1. Logic to handle validating input from a client and reacting accordingly:
           a. If the input is invalid, sending the client an error message.
           b. If the input is valid, establishing a TCP data connection to send
              appropriate data (file or directory) to a client, and closing that
              connection once everything is transmitted.
        2. Ceasing to waiting on a client once that client closes the TCP control connection.
        3. Closing the TCP control connection once a termination signal is recieved.
        """        
        try:
            conn, addr = self.listen.accept()
            print 'Accepted client at address: ' + addr

            while True:
                data = conn.recv(self.BUFFER_SIZE)
            
                if not data:
                    break

                cmd_list = data.split()

                if valid_cmd(cmd_list[0]):
                    if cmd_list[0] == 'list':
                        print 'got a list command!'
                        conn.send('1')
                    else:
                        print 'got a get command!'
                        conn.send('1')

                    # initialize TCP data connection and do work son
                else:
                    print('Uh-oh, should probably send an error message here!')
                    conn.send('0 ERROR: command not supported.')
            conn.close()
        except KeyboardInterrupt:
            pass
        finally:
            print '\nExiting...'

    def valid_cmd(self, cmd):
        """Checks to see if command sent from server is a 'list' or 'get' command. """
        return cmd == 'list' or cmd == 'get'

# Enty point for the application.
# Intantiates and starts the server.
if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print 'usage: ftserv [host]'
    else:
        server = ftserv(sys.argv[1])
        server.start()
