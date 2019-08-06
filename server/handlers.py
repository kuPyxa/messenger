import json
import logging

from protocol import validate_request, make_response
from actions import resolve
from middlewares import compression_middleware, encryption_middleware


@compression_middleware
@encryption_middleware
def handle_default_request(bytes_request):
    request = json.loads(bytes_request.decode())

    if validate_request(request):
        action_name = request.get('action')
        controller = resolve(action_name)
        if controller:
            try:
                logging.info('Client sent valid request')
                response = controller(request)
            except Exception as err:
                logging.critical(f'Internal server error: {err}')
                response = make_response(request, 500, data='Internal server error')
        else:
            logging.error(f'Controller with action name {action_name} does not exist')
            response = make_response(request, 404, data='Action not found')
    else:
        logging.error('Client sent wrong request')
        response = make_response(request, 400, data='Wrong request')

    j_response = json.dumps(response)
    return j_response.encode()
