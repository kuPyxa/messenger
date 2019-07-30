import yaml
from argparse import ArgumentParser
import socket
import json
import logging

from server.protocol import validate_request, make_response
from server.actions import resolve

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


logger = logging.getLogger('main')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('main.log')
stream_handler = logging.StreamHandler()

file_handler.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    logger.info(f'Server started with {host}:{port}')

    while True:
        client, address = sock.accept()
        logger.info(f'Client was detected {address[0]}:{address[1]}')

        b_request = client.recv(buffer_size)
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    logger.info('Client sent valid request')
                    response = controller(request)
                except Exception as err:
                    logger.critical(f'Internal server error: {err}')
                    response = make_response(request, 500, data='Internal server error')
            else:
                logger.error(f'Controller with action name {action_name} does not exist')
                response = make_response(request, 404, data='Action not found')
        else:
            logger.error('Client sent wrong request')
            response = make_response(request, 400, data='Wrong request')

        j_response = json.dumps(response)
        client.send(j_response.encode())

        client.close()
except KeyboardInterrupt:
    print('Server shutdown')
