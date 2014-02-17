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
    HOST = 'A'
    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024

    def start(self):
        """
        Routine which handles the following:
        1. Initializing components to listen on a TCP control connection.
        2. Initializing component which continuously waits on input from a client
        3. Logic to handle validating input from a client and reacting accordingly:
           a. If the input is invalid, sending the client an error message.
           b. If the input is valid, establishing a TCP data connection to send
              appropriate data (file or directory) to a client, and closing that
              connection once everything is transmitted.
        4. Ceasing to waiting on a client once that client closes the TCP control connection.
        5. Closing the TCP control connection once a termination signal is recieved.
        """
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen.bind((self.HOST, self.CTRLPORT))
        self.listen.listen(1)
        
        try:
            conn, addr = self.listen.accept()
            print('Accepted client at address: ', addr)

            while True:
                data = conn.recv(self.BUFFER_SIZE)
            
                if not data:
                    break

                cmd_list = data.split()

                if valid_cmd(cmd_list[0]):
                    if cmd_list[0] == 'list':
                        print('got a list command!\n')
                        conn.send('1')
                    else:
                        print('got a get command!\n')
                        conn.send('1')
                else:
                    print('Uh-oh, should probably send an error message here!\n')
                    conn.send('0 ERROR: command not supported.\n')
            conn.close()
        except (KeyboardInterrupt):
            pass
        finally:
            print('\nExiting...')

    def valid_cmd(self, cmd):
        ''' Checks to see if command sent from server is a 'list' or 'get' command. '''
        return cmd == 'list' or cmd == 'get'

# Enty point for the application.
# Intantiates and starts the server.
if __name__ == "__main__":
    server = ftserv()
    server.start()
