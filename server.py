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
    sock.bind((host, port))
    sock.listen(5)

    print(f'Server started with {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client was detected {address[0]}:{address[1]}')

        b_request = client.recv(buffer_size)
        payload_client = json.loads(b_request.decode())
        message = payload_client['message']
        print(f'Client sent message: {message}')

        if message:
            payload_server = json.dumps({'code': 0})
        else:
            payload_server = json.dumps({'code': 1})
        client.send(payload_server.encode())
        client.close()
except KeyboardInterrupt:
    print('Server shutdown')
