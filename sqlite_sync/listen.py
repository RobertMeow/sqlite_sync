import json
import socket


class ListeningSocket:
    __slots__ = ('_addr', '_buffer_size', '_socket')

    def __init__(self, address: str, buffer_size: int = 16384):
        self._addr = address
        self._buffer_size = buffer_size
        self._socket = socket.socket(socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(self._addr)
        self._socket.listen()

    def listen(self):
        while True:
            conn, addr = self._socket.accept()
            with conn:
                try:
                    data = conn.recv(self._buffer_size)
                except KeyboardInterrupt:
                    conn.close()
                    self._socket.close()
                    break
                yield json.loads(data), conn


class Listen:
    @staticmethod
    def listen(config):
        sock = ListeningSocket(config)
        for data, conn in sock.listen():
            yield data, conn
