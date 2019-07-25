from protocol import make_response


def send_message(request):
    data = request.get('data')
    return make_response(request, 200, data)
