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

    HOST = 'B'
    CTRLPORT = 30021
    DATAPORT = 30020
    BUFFER_SIZE = 1024

    def __init__(self):
        """ Initialization routine.  Connects to port 30021. """
        self.ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ctrl_sock.connect((HOST, CTRLPORT))

        print('Connected over host B on port 30021.\n')        

    def start(self, cmd, file):
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
        if cmd == 'get':
            cmd = cmd + ' ' + file

        send(cmd)
        data = self.ctrl_sock.recv(BUFFER_SIZE)
            
        if data:           
            data = data.split()
            if int(data[0]) == 0:
                print(data[1])
            else:
                # Connect to Q, get data from it, print that out
                print('')
        
        print('Finished getting data.  Closing...\n')    
        self.ctrl_sock.close()



# Enty point for the application.
# Intantiates and starts the client.
if __name__ == "__main__":
    if not len(sys.argv) > 1 and not len(sys.argv) <= 3:
        print('usage: ftclient [command] (optional)[filename]')
        exit(1)
    client = ftclient()
    if len(sys.argv) == 2:
        client.start(sys.argv[1], '')
    else:
        client.start(sys.argv[1], sys.argv[2])