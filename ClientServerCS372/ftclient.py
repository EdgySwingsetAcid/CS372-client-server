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

        print 'Connected over host B on port 30021.\n'        

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
        try:
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
                    print ''
        
            print 'Finished getting data.\n'    
            self.ctrl_sock.close()
        except KeyboardInterrupt:
            pass
        finally:
            print '\nExiting...'



# Enty point for the application.
# Intantiates and starts the client.
if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print 'usage: ftclient [host] [command] (optional)[filename]'
    else:
        client = ftclient(sys.argv[1])
        if len(sys.argv) == 2:
            client.start(sys.argv[2], '')
        else:
            client.start(sys.argv[2], sys.argv[3])