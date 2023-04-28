from sqlite_sync import ClientDriver, HandlerDB
from threading import Thread
import time


def test(client: ClientDriver):
    while True:
        client.save("INSERT INTO test (name, age) VALUES ('Robert', 18)")
        time.sleep(0.1)


def main(config):
    db = HandlerDB(':memory:', config)
    client = ClientDriver(config)

    client.save("CREATE TABLE test (name TEXT, age INTEGER)")

    for i in range(10):
        Thread(target=test, args=(client,)).start()

    # db.HD.kill()


if __name__ == '__main__':
    config = ('127.0.0.1', 5001)
    main(config)
