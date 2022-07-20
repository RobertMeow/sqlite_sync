import json
import time
import traceback

from .control_db import Driver
from .listen import Listen

from multiprocessing import Process


class HandlerDB(Driver, Listen):
    __slots__ = ["HD"]

    def __init__(self, warp_file=':memory:', config=("localhost", 1001)):
        super().__init__(warp_file)
        self.config = config
        self.HD = Process(target=self.handler, name='HANDLER_DB')
        self.HD.start()
        time.sleep(0.1)

    def handler(self):
        while True:
            try:
                for data in self.listen(self.config):
                    response = data[0]
                    if 'query' in response and 'type' in response:
                        match response['type']:
                            case 'save':
                                result = self.save(response['query'])
                            case 'receive':
                                result = self.receive(response['query'])
                            case 'receives':
                                result = self.receives(response['query'])
                            case _:
                                result = 'Неизвестный запрос!', None
                        data[1].send(bytes(json.dumps({'result': result[0], 'status': result[1]}), encoding='UTF-8'))
            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()

    def __del__(self):
        self.HD.kill()
