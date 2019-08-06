import yaml
from argparse import ArgumentParser
import socket
import logging
import select

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

requests = []
connections = []

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
    sock.setblocking(False)
    sock.settimeout(0)
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client was detected {address[0]}:{address[1]}')
            connections.append(client)
        except:
            pass

        if connections:
            rlist, wlist, xlist = select.select(connections, connections, connections, 0)

            for read_client in rlist:
                try:
                    b_request = read_client.recv(buffer_size)
                except Exception:
                    connections.remove(read_client)
                else:
                    requests.append(b_request)

            if requests:
                b_request = requests.pop()
                b_response = handle_default_request(b_request)
                for write_client in wlist:
                    try:
                        write_client.send(b_response)
                    except Exception:
                        connections.remove(write_client)
except KeyboardInterrupt:
    print('Server shutdown')
