import json
import socket


class ErrorDB(Exception):
    def __init__(self, desc):
        self.desc = desc


class ClientDriver:
    __slots__ = ['con', 'sql', 'port', 'ip', 'pid']

    def __init__(self, handler):
        self.ip, self.port = handler.config[0], handler.config[1]

    def send(self, query: str, type_method: str):
        sock = socket.socket(socket.SOCK_DGRAM)
        sock.connect((self.ip, self.port))
        sock.send(bytes(json.dumps({'query': query, 'type': type_method}), encoding='UTF-8'))
        data = b""
        while True:
            packet = sock.recv(32)
            if not packet:
                break
            data += packet
        sock.close()
        data = json.loads(data)
        if not data['status']:
            raise ErrorDB(data['result'])
        return data['result']

    def receive(self, query: str):
        return self.send(query, 'receive')

    def receives(self, query: str):
        return self.send(query, 'receives')

    def save(self, query: str):
        return self.send(query, 'save')
