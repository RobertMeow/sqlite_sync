import socket, json


while True:
    sock = socket.socket(socket.SOCK_DGRAM)
    sock.connect(('127.0.0.1', 101))
    sock.send(bytes(json.dumps({'query': "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name='users'", 'type': 'receive'}), encoding='UTF-8'))
    data = sock.recv(1024)
    print(json.loads(data))
    sock.close()
