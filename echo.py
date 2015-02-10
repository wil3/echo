#!/usr/bin/env python
import socket
import sys
import argparse
"""
  This script is used to perform a network echo of a message. Whitespaces are used to parse command line parameters, for messages including spaces surrond with quotes.

  Usage: python echo.py host port message

  Example: python echo.py csa2.bu.edu 5000 "hello world"

  By William Koch
"""

#Buffer size for receiving data
BUFFER_SIZE = 2048
class Echo:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def run(self,msg):
        """
        Create a socket, send message to server, and print reply
        """
        try:                
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host,self.port))
            self.sendall(msg)
            data = self.recvall(len(msg))
            print data
        except Exception as e:
            print str(e)
        finally:
            self.sock.close()
    
    def sendall(self, msg):
        """
        Send the entire message
        """
        totalsent=0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Could not send message")
            totalsent = totalsent + sent

    def recvall(self, msg_len):
        """
        Receive the specified number of bytes and return the 
        result. Message is received in chunks and then combined together
        while fully received
        """
        chunks = []
        bytesrecv = 0
        while bytesrecv < msg_len:
            chunk = self.sock.recv(min(msg_len - bytesrecv, BUFFER_SIZE))
            if chunk == '':
                raise RuntimeError("Could not receive message")
            chunks.append(chunk)
            bytesrecv = bytesrecv + len(chunk)
        return ''.join(chunks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Echo string to a server.')
    parser.add_argument('host',  help='Server address')
    parser.add_argument('port', type=int, help='Server port')
    parser.add_argument('message',  help='Message to echo')
    args = parser.parse_args()
    e = Echo(args.host,args.port)
    e.run(args.message)




