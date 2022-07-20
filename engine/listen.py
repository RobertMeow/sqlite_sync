import json
import socket


class Listen:
    @staticmethod
    def listen(config):
        sock = socket.socket(socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(config)
        sock.listen()
        while True:
            conn, addr = sock.accept()
            with conn:
                data = conn.recv(16384)
                yield json.loads(data), conn
