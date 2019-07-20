import yaml
from argparse import ArgumentParser
import socket


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

    data = input('Enter data:')

    sock.send(data.encode())
    print(f'Client sent data {data}')

    b_response = sock.recv(buffer_size)
    print(f'Server sent data {b_response.decode()}')
except KeyboardInterrupt:
    print('Client shutdown')
