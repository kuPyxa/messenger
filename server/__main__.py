import yaml
from argparse import ArgumentParser
import socket
import json

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

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    print(f'Server started with {host}:{port}')

    while True:
        client, address = sock.accept()
        print(f'Client was detected {address[0]}:{address[1]}')

        b_request = client.recv(buffer_size)
        request = json.loads(b_request.decode())

        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    print('Client sent valid request')
                    response = controller(request)
                except Exception as err:
                    print(f'Internal server error: {err}')
                    response = make_response(request, 500, data='Internal server error')
            else:
                print(f'Controller with action name {action_name} does not exist')
                response = make_response(request, 404, data='Action not found')
        else:
            print('Client sent wrong request')
            response = make_response(request, 404, data='Wrong request')

        j_response = json.dumps(response)
        client.send(j_response.encode())

        client.close()
except KeyboardInterrupt:
    print('Server shutdown')
