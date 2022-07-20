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
            data = b""
            conn, addr = sock.accept()
            while True:
                packet = conn.recv(32)
                if not packet:
                    break
                data += packet
            yield json.loads(data), conn
            conn.close()
