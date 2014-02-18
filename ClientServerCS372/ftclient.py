import os
import socket
import sys

class ftclient:
    """
    Client end of the application.

    Contains routines to establish and connect to a TCP data connection to a server,
    send commands to the server, recieve data, and process and display that data.

    Author: Phillip Carter
    Class: CS 372, Winter 2014
    Last Modified: 2/17/2014
    """

    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024

    def __init__(self, host):
        """ Initialization routine.  Connects to port 30021. """
        self.ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ctrl_sock.connect((host, self.CTRLPORT))

        print 'Connected over host B on port 30021.'        

    def start(self, host, cmd, file):
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
            if cmd == 'get':
                cmd = cmd + ' ' + file

            self.ctrl_sock.send(cmd)
            data = self.ctrl_sock.recv(self.BUFFER_SIZE)
            
            if data:           
                data = data.split()

                if int(data[0]) == 0:
                    print ' '.join(map(str, data[1:]))
                else:
                    # Connect to Q, get data from it, print that out
                    self.connect_for_data(host)
                    self.handle_data()
                    self.data_sock.close()
        
            print 'Finished getting data.'    
            self.ctrl_sock.close()
        except KeyboardInterrupt:
            pass
        finally:
            print '\nExiting...'

    def connect_for_data(self, host):
        """ Establishes a TCP Data connection on port 320020 """
        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock.connect((host, self.DATAPORT))

    def handle_data(self):
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
                print os.listdir(data)
            else:
                print 'durrr'
                # save the file in the current directory

# Enty point for the application.
# Intantiates and starts the client.
if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print 'usage: ftclient [host] [command] (optional)[filename]'
    else:
        client = ftclient(sys.argv[1])
        if len(sys.argv) == 3:
            client.start(sys.argv[1], sys.argv[2], '')
        else:
            client.start(sys.argv[1], sys.argv[2], sys.argv[3])