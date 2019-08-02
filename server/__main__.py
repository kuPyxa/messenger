import yaml
from argparse import ArgumentParser
import socket
import logging

from handlers import handle_default_request


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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    while True:
        client, address = sock.accept()
        logging.info(f'Client was detected {address[0]}:{address[1]}')

        b_request = client.recv(buffer_size)
        b_response = handle_default_request(b_request)

        client.send(b_response)
        client.close()
except KeyboardInterrupt:
    print('Server shutdown')
