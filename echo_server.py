#!/usr/bin/env python

"""
Echo server used in conjunction with echo client echo.py.
This server will echo back any data it receives.

Usage: python echo_server.py port

Example: python echo_server.py 5000

By William Koch
"""


import socket
import sys
import multiprocessing
import argparse
from server import *


class EchoHandler(ServerHandler):
    """
    This class is a handler for when the server spawns a new process
    for the connection in which the function handle is called. The
    majority of the work is done in server.py
    """

    def __init__(self):
        pass
    def handle(self):
        """
        Handle the new connection, echo back any data received
        """
        while 1:
            try:
                data = self.conn.recv(1024)
                if not data: break
                print ("[%s:%s]\t%s" % (self.addr[0],self.addr[1],data))
                self.conn.send(data)
            except Exception as e:
                print "Error echo data", str(e)
                break
        #Only close connection when done receiving 
        #all data or when an error occurs
        self.conn.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Echo server.')
    parser.add_argument('port',type=int, help='Server port')
    args = parser.parse_args()
    server = Server(args.port)
    es = EchoHandler()
    server.run(es)

    print "Bye!" 
