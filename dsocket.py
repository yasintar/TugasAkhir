import socket
import os
import sys
from data import Data
import threading
import pickle

class dataSender:
    def __init__(self, address='127.0.0.1', port='5000') -> None:
        self.address = address
        self.port = port
        self.client = None

    def open_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
    
    def close_socket(self):
        self.client.close()
        sys.exit(0)

    def send_data(self, receiver, filename):
        data = Data(self.client.getsockname(), receiver, 
                    filename, os.path.getsize("images/"+filename))
        data = pickle.dumps(data)
        self.client.send(data)

class dataReceiver:
    def __init__(self, address='127.0.0.1', port='5000') -> None:
        self.address = address
        self.port = port
        self.server = None

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        self.connection, self.sender_address = self.server.accept()
        print("Connected to -> {}".format(self.sender_address))
        while True:
            res = b''
            while True:
                recv_data = self.connection.recv(1024)
                res += recv_data
                if len(recv_data)<1024-1:
                    break
            data = 
            