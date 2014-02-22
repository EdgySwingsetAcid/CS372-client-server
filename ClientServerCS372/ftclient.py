import os
import socket
import sys
import errno
import time

class ftclient:
    """
    Client end of the application.

    Contains routines to establish and connect to a TCP data connection to a server,
    send commands to the server, recieve data, and process and display that data.

    Author: Phillip Carter
    Class: CS 372, Winter 2014
    Last Modified: 2/22/2014
    """

    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024
    MAX_ATTEMPTS = 5

    def __init__(self, host, port):
        """ Initialization routine.  Connects to port 30021. """
        self.ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ctrl_sock.connect((host, port))

        print 'Connected over host B on port 30021.'        

    def start(self, host):
        """
        Handles the following:
        1. Adjusting command to send to server
        2. Sends command to server over TCP Contol connection
        3. Gets data back over TCP control connection:
           a. If data is an error message, prints the message.
           b. If data signifies it was a valid command,
              calls routine that establishes and works on a TCP data connection.
        4. Closes the TCP data connection.
        """
        try:
            self.attempt_login()
            while True:
                file_flag = False
                cmd = raw_input('Enter a command, or hit enter to exit: ')
                if not cmd.strip():
                    break
                
                if 'get' in cmd:
                    tmp = cmd.split()
                    if len(tmp) > 1:
                        filename = tmp[1]
                        file_flag = True

                self.ctrl_sock.send(cmd)
                data = self.ctrl_sock.recv(self.BUFFER_SIZE)
            
                if data:           
                    data = data.split()

                    # If the data we got back is an error, print it out.
                    # Otherwise, it's time for some real data!
                    if int(data[0]) == 0:
                        print ' '.join(map(str, data[1:]))
                    else:
                        # Connect to Q, get data from it, print that out
                        try:
                            self.connect_for_data(host)
                        except RuntimeError as ex:
                            if ex.message == 'Max number of unsuccessful attempts reached':
                                continue

                        if file_flag:
                            if os.path.exists(filename):
                                print 'File already exists in this directory.'
                                continue
                            else:
                                self.handle_data(filename)
                        else:
                            self.handle_data('')
                        print 'Closing data connection...'
                        self.data_sock.close()
        except KeyboardInterrupt:            
            pass
        finally:         
            print 'Closing control connection...'
            self.ctrl_sock.close()
            print '\nExiting...'

    def attempt_login(self):
        while True:
            login = raw_input('Enter a username: ')
            pwd = raw_input('Enter the password: ')
            self.ctrl_sock.send(login + pwd)
            if self.ctrl_sock.recv(self.BUFFER_SIZE) == 'success':
                print 'Success!\n'
                break
            else:
                print 'Login error.  Try again.'

    def connect_for_data(self, host):
        """ 
        Attempts to establish a TCP Data connection over port 320020.
        If it cannot connect 5 times, it raises a runtime error
        and the client will exit.
        """
        for attempt in range(self.MAX_ATTEMPTS):
            try:
                self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_sock.connect((host, self.DATAPORT))
                print 'Connected to a data connection over port 320020...'
            except EnvironmentError as exc:
                if exc.errno == errno.ECONNREFUSED:
                    print 'Connection failure; trying again in 1 second...'
                    time.sleep(1)
                else:
                    raise
            else:
                break
        else:
            raise RuntimeError("Max number of unsuccessful attempts reached")

    def handle_data(self, file):
        """
        Handles incoming data from the server.

        If the received data is a directory string:
            - prints the contents of that directory.
        Else:
            - Saves the stringified file contents as a file
            - prints message
        """
        data = self.data_sock.recv(self.BUFFER_SIZE)
        if data:
            if os.path.isdir(data):
                print '\nCurrent directory contents:'
                print '\n'.join(os.listdir(data))
            else:
                print 'Got the file!  Writing to directory...'
                with open(file, 'w+') as the_file:
                    the_file.write(data)
                print 'durrr'
                # save the file in the current directory

# Enty point for the application.
# Intantiates and starts the client.
if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print 'usage: ftclient [host] [port]'
    else:
        client = ftclient(sys.argv[1], int(sys.argv[2]))
        client.start(sys.argv[1])