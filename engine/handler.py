import json, traceback

from .app import listen
from . import DB


def handler():
    while True:
        try:
            for data in listen():
                response = data[0]
                if 'query' in response and 'type' in response:
                    match response['type']:
                        case 'save':
                            result = DB.save(response['query'])
                        case 'receive':
                            result = DB.receive(response['query'])
                        case 'receives':
                            result = DB.receives(response['query'])
                        case _:
                            result = None
                    data[1].send(bytes(json.dumps({'result': result, 'status': 'success' if result is not None else 'error'}), encoding='UTF-8'))
        except KeyboardInterrupt:
            break
        except:
            traceback.print_exc()
