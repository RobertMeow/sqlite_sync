import socket, json
from . import config

sock = socket.socket(socket.SOCK_DGRAM)
sock.bind((config['listen_ip'], config['port']))
sock.listen()


def listen():  # {"query": ""}
    print('START LISTEN')
    while True:
        conn, addr = sock.accept()
        data = conn.recv(16384*16)  # 16384
        print(data)
        yield json.loads(data), conn
        conn.close()
