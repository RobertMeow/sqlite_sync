import socket, json


def send(query, type):
    sock = socket.socket(socket.SOCK_DGRAM)
    sock.connect(('94.228.116.191', 101))
    sock.send(bytes(json.dumps({'query': query, 'type': type}), encoding='UTF-8'))
    data = sock.recv(1024)
    sock.close()
    return json.loads(data)
