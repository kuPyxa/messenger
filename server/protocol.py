from datetime import datetime


def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    else:
        return False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': datetime.now().timestamp(),
        'code': code,
        'data': data
    }
