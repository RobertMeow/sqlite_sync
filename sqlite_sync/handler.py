import json
import time
import traceback

from .control_db import Driver
from .listen import Listen

from multiprocessing import Process, Event
from threading import Thread
from sys import platform


class HandlerDB(Driver, Listen):
    __slots__ = ["HD", "config"]

    def __init__(self, warp_file=':memory:', config=("127.0.0.1", 1001)):
        super().__init__(warp_file)
        self.config = config
        self.event = Event()
        if platform not in ['darwin', 'win32']:
            self.HD = Process(target=self.handler, name='HANDLER_DB')
            self.HD.start()
        else:
            self.HD = Thread(target=self.handler, name='HANDLER_DB')
            self.HD.start()
        time.sleep(0.1)

    def handler(self):
        while not self.event.is_set():  # sooner or later...
            try:
                for data in self.listen(self.config):
                    response = data[0]
                    if 'query' in response and 'type' in response:
                        """match response['type']:
                            case 'save':
                                result = self.save(response['query'])
                            case 'receive':
                                result = self.receive(response['query'])
                            case 'receives':
                                result = self.receives(response['query'])
                            case _:
                                result = 'Unknown request!', None"""  # this is a new feature in python 3.10
                        if response['type'] == 'save':
                            result = self.save(response['query'])
                        elif response['type'] == 'receive':
                            result = self.receive(response['query'])
                        elif response['type'] == 'receives':
                            result = self.receives(response['query'])
                        else:
                            result = 'Unknown request!', None
                        data[1].send(bytes(json.dumps({'result': result[0], 'status': result[1]}), encoding='UTF-8'))
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()

    def kill(self):
        if platform not in ['darwin', 'win32']:
            self.HD.terminate()
        else:
            self.event.set()
        # self.event.set()  # TODO: Maybe use this?
