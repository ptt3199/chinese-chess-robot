import json
import socket


class Client:
    def __init__(self, port=8080):
        self.socket = socket.socket()
        self.addrHost = (socket.gethostname(), port)
        self.socket.connect(self.addrHost)

    def send(self, data):
        jsonObj = json.dumps(data)
        self.socket.sendto(bytes(jsonObj, 'utf-8'), self.addrHost)

    def receive(self):
        dataReceive = str(self.socket.recv(1024))
        return json.loads(dataReceive[2:len(dataReceive) - 1])

    def close(self):
        self.socket.close()


class Server:
    def __init__(self, port=8080):
        self.socket = socket.socket()
        self.socket.bind((socket.gethostname(), port))
        self.socket.listen(1)
        self.conn = None
        self.address = None

    def accept(self):
        self.conn, self.address = self.socket.accept()

    def send(self, data):
        jsonObj = json.dumps(data)
        self.conn.send(bytes(jsonObj, 'utf-8'))

    def receive(self):
        dataReceive = str(self.conn.recv(1024))
        return json.loads(dataReceive[2:len(dataReceive) - 1])

    def close(self):
        self.socket.close()
        self.address = None
        self.conn = None
