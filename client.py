import yaml
from argparse import ArgumentParser
import socket
import json

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

    message = input('Enter message:')

    payload_client = json.dumps({'message': message})

    sock.send(payload_client.encode())
    print(f'Client sent message: {message}')

    b_response = sock.recv(buffer_size)
    payload_server = json.loads(b_response.decode())
    code = payload_server['code']
    print(f'Server sent code {code}')
except KeyboardInterrupt:
    print('Client shutdown')
