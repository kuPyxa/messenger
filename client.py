import yaml
from argparse import ArgumentParser
import socket
import json
from datetime import datetime
import zlib
import threading


def read(sock, buffer_size):
    while True:
        response = sock.recv(buffer_size)
        b_response = zlib.decompress(response)
        print(b_response.decode())


def make_request():
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': message
    }


parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False, help='Set config file path'
)

args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000,
    'buffer_size': 1024
}

if args.config:
    with open(args.config) as f:
        file_config = yaml.load(f, Loader=yaml.Loader)
        config.update(file_config)

host, port = config.get('host'), config.get('port')
buffer_size = config.get('buffer_size')

try:
    sock = socket.socket()
    sock.connect((host, port))
    print('Client was started')

    read_thread = threading.Thread(target=read, args=(sock, buffer_size))
    read_thread.start()

    while True:
        action = input('Enter action: ')
        message = input('Enter message: ')

        request = make_request()
        j_request = json.dumps(request)
        b_request = zlib.compress(j_request.encode())

        sock.send(b_request)
        print(f'Client sent request: {request}')
except KeyboardInterrupt:
    print('Client shutdown')
