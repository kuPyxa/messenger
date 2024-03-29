import yaml
from argparse import ArgumentParser
import socket
import logging
import select
import threading

from handlers import handle_default_request


def read(sock, connections, requests, buffer_size):
    try:
        b_request = sock.recv(buffer_size)
    except ConnectionResetError:
        pass
    except Exception:
        connections.remove(read_client)
    else:
        requests.append(b_request)


def write(sock, connections, b_response):
    try:
        sock.send(b_response)
    except ConnectionResetError:
        pass
    except Exception:
        connections.remove(write_client)


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
                read_thread = threading.Thread(target=read, args=(read_client, connections, requests, buffer_size))
                read_thread.start()

            if requests:
                b_request = requests.pop()
                b_response = handle_default_request(b_request)
                for write_client in wlist:
                    write_thread = threading.Thread(target=write, args=(write_client, connections, b_response))
                    write_thread.start()
except KeyboardInterrupt:
    print('Server shutdown')
