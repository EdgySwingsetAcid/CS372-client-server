import sys
import os
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

    HOST = 'localhost'
    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024

    def __init__(self):
        """
        Initialization routine.
        1. Initializing components to listen on a TCP control connection.
        2. Initializing component which continuously waits on input from a client
        """

        print 'Connecting over host A on port 30021...'

        self.ctrlsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ctrlsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ctrlsock.bind((self.HOST, self.CTRLPORT))
        self.ctrlsock.listen(1)

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
            ctrlconn, ctrladdr = self.ctrlsock.accept()
            print 'Client connected!'
            while True:
                print 'Waiting on client...'
                data = ctrlconn.recv(self.BUFFER_SIZE)
            
                if data:
                    cmd_list = data.split()

                    if self.valid_cmd(cmd_list[0]):
                        if cmd_list[0] == 'list':
                            print 'Received list command.'
                            ctrlconn.send('1')
                            self.service_client(cmd_list, True)
                        else:
                            print 'Received get command.'
                            ctrlconn.send('1')
                            if len(cmd_list) > 1 and self.valid_file(cmd_list[1]):
                                self.service_client(cmd_list, False)
                            else:
                                ctrlconn.send('0 ERROR: file does not exist in current directory.')                    
                    else:
                        conn.send('0 ERROR: command not supported.')
        except KeyboardInterrupt:
            pass
        finally:
            print 'Closing control connection...'
            ctrlconn.close()
            print '\nExiting...'

    def service_client(self, cmd_list, list_flag):
        """
        Utility function which sets up a TCP data connection,
        accepts a connection, and sends either the current working directory
        or the contents of the requested file.

        Precondition:  if list_flag is false, cmd_list[1] is a valid file.
        """
        self.init_data_conn()
        dataconn, dataaddr = self.datasock.accept()

        if list_flag:
            dataconn.send(os.getcwd())
            print 'Current Working Directory sent!'
        else:
            with open(cmd_list[1]) as file:
                data = data = "".join(line.rstrip() for line in file)
            dataconn.send(data)
        print 'Closing data connection...'
        dataconn.close()

    def init_data_conn(self):
        """ Initializes a TCP data connection on port 30020. """
        print 'Connecting over host A on port 30020...'

        self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.datasock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.datasock.bind((self.HOST, self.DATAPORT))
        self.datasock.listen(1)

    def valid_cmd(self, cmd):
        """Checks to see if command sent from server is a 'list' or 'get' command. """
        return cmd == 'list' or cmd == 'get'
    
    def valid_file(self, path):
        """ Checks that a file exists in the cwd and is a file (not directory). """
        return os.path.exists(path) and os.path.isfile(path)

    def get_cwd(self):
        """ Assembles the current working directory as a string """
        return os.getcwd()

# Enty point for the application.
# Intantiates and starts the server.
if __name__ == "__main__":
    server = ftserv()
    server.start()
