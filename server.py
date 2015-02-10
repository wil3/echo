"""
Main server that handles connections and kicks off a process
for each one. When a connection is received a handler function is 
called. 

To use this class create a handler class and subclass ServerHandler
and override handle function.


By William Koch
"""

import socket
import multiprocessing

HOST = '' # Symbolic name meaning the local host

class Server:

    def __init__(self, port):
        self.port = port

    def run(self, handler):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # For testing allow socket reuse so we can 
            # quicker re-run the Server
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, self.port))
            s.listen(1)

            print ("Server running on port %d" % self.port)
            while 1:
                conn, addr = s.accept()
                handler.set_conn(conn)
                handler.set_addr(addr)

                process = multiprocessing.Process(target=handler.handle) 
                process.daemon = True
                process.start()

        finally: #Do clean up
            for process in multiprocessing.active_children():
                process.terminate()
                process.join()


class ServerHandler:
    """
    Subclass this class and override handle function 
    to handle server connections
    """

    def set_conn(self,conn):
        self.conn = conn
    def set_addr(self,addr):
        self.addr = addr
    def handle(self):
        raise NotImplementedError("Need to implemented the handle")

