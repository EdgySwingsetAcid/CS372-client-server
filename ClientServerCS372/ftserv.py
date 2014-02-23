import sys
import os
import socket

class cd:
    """
    Small class to handle saving the original cwd,
    changing to a given directory, and reverting
    back to the original cwd.
    """
    def __init__(self):
        """ 
        Saves the original current working directory.
        This is so the server can get back to its original
        directory before terminating.
        """
        self.origin = os.getcwd()

    def go(self, path):
        os.chdir(path)

    def revert(self):
        if not os.getcwd() == self.origin:
            os.chdir(self.origin)



class ftserv:
    """
    Class which represents the ftserv server.

    Contains routines to initialize components and listen for clients,
    receive data, validate commands sent from clients, and send data
    to clients over a TCP data connection.

    Author: Phillip Carter
    Class: CS 372, Winter 2014
    Last Modified: 2/22/2014
    """

    HOST = 'localhost'
    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024
    USERNAME = 'GuruOfFunk'
    PWD = 'Funkify'

    valid_cmds = ['list', 'get', 'cd']

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

        self.cd = cd()
        try:
            ctrlconn, ctrladdr = self.ctrlsock.accept()
            print 'Client connected!'

            self.do_login(ctrlconn)

            while True:
                print 'Waiting on client to send command...'
                data = ctrlconn.recv(self.BUFFER_SIZE)
            
                if data:
                    cmd_list = data.split()

                    if self.valid_cmd(cmd_list[0]):
                        if cmd_list[0] == 'get':
                            print 'Received get command.'
                            if len(cmd_list) > 1 and self.valid_file(cmd_list[1]):
                                ctrlconn.send('1')
                                self.service_client(cmd_list)
                            else:
                                ctrlconn.send('0 ERROR: file does not exist in current directory.')
                        elif cmd_list[0] == 'list':
                            print 'Received list command.'
                            ctrlconn.send('1')
                            self.service_client(cmd_list)
                        elif cmd_list[0] == 'cd':
                            print 'Received cd command.'
                            if len(cmd_list) > 1 and os.path.isdir(cmd_list[1]):
                                ctrlconn.send('1')
                                self.service_client(cmd_list)
                            else:
                                ctrlconn.send('0 ERROR: no valid directory path given.')
                                               
                    else:
                        ctrlconn.send('0 ERROR: command not supported.')
                else:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            self.cd.revert()
            print 'Closing control connection...'
            self.ctrlsock.close()
            print '\nExiting...'

    def do_login(self, ctrlconn):
        """ Continuously checks a user login attempt until it's valid. """
        while True:
            data = ctrlconn.recv(self.BUFFER_SIZE)
            if data and data == self.USERNAME + self.PWD:
                ctrlconn.send('success')
                break
            else:
                ctrlconn.send('failure')


    def service_client(self, cmd_list):
        """
        Utility function which handles a client command.
        (a) Changes the current working directory
        (b) establishes a TCP data connection, and:
            (1) Gets a named file from the current working directory and
                sends it to the client, or
            (2) Sends the current working directory to the client.
        """

        if cmd_list[0] == 'cd':
            self.cd.go(cmd_list[1])
            print 'Changed directory!'
        else:
            self.init_data_conn()
            dataconn, dataaddr = self.datasock.accept()

            if cmd_list[0] == 'get':
                with open(cmd_list[1]) as file:
                    data = data = "".join(line.rstrip() for line in file)
                dataconn.send(data)
            elif cmd_list[0] == 'list':
                dataconn.send(os.getcwd())
                print 'Current Working Directory sent!'

            dataconn.close()

    def init_data_conn(self):
        """ Initializes a TCP data connection on port 30020. """
        print 'Establishing data connection on port 30020...'

        self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.datasock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.datasock.bind((self.HOST, self.DATAPORT))
        self.datasock.listen(1)

    def valid_cmd(self, cmd):
        """Checks to see if command sent from server is a 'list' or 'get' command. """
        return cmd in self.valid_cmds
    
    def valid_file(self, path):
        """ Checks that a file exists in the cwd and is a file (not directory). """
        return os.path.exists(path) and os.path.isfile(path)

# Enty point for the application.
# Intantiates and starts the server.
if __name__ == "__main__":
    server = ftserv()
    server.start()
