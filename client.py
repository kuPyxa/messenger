import yaml
from argparse import ArgumentParser
import socket
import json
from datetime import datetime

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

    action = input('Enter action: ')
    data = input('Enter message: ')

    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }

    j_request = json.dumps(request)

    sock.send(j_request.encode())
    print(f'Client sent request: {request}')

    b_response = sock.recv(buffer_size)
    response = json.loads(b_response.decode())
    print(f'Server sent response {response}')
except KeyboardInterrupt:
    print('Client shutdown')
