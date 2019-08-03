import pytest
from datetime import datetime
import json
import zlib

from handlers import handle_default_request


@pytest.fixture
def valid_action():
    return 'echo'


@pytest.fixture
def valid_data():
    return 'Some data'


@pytest.fixture
def valid_code():
    return 200


@pytest.fixture
def invalid_data():
    return 'Wrong request'


@pytest.fixture
def invalid_code():
    return 400


@pytest.fixture
def valid_request(valid_action, valid_data):
    return {
        'action': valid_action,
        'time': datetime.now().timestamp(),
        'data': valid_data
    }


@pytest.fixture
def invalid_request():
    return {
        'invalid_key': 'invalid_value'
    }


class TestRequests:
    @staticmethod
    def encoding_request(request):
        b_request = json.dumps(request).encode()
        c_request = zlib.compress(b_request)
        return c_request

    @staticmethod
    def decoding_request(response):
        d_response = zlib.decompress(response)
        response = json.loads(d_response)
        return response

    def test_data_valid_request(self, valid_request, valid_data):
        c_request = self.encoding_request(valid_request)
        b_response = handle_default_request(c_request)
        response = self.decoding_request(b_response)
        assert response.get('data') == valid_data

    def test_code_valid_request(self, valid_request, valid_code):
        c_request = self.encoding_request(valid_request)
        b_response = handle_default_request(c_request)
        response = self.decoding_request(b_response)
        assert response.get('code') == valid_code

    def test_data_invalid_request(self, invalid_request, invalid_data):
        c_request = self.encoding_request(invalid_request)
        b_response = handle_default_request(c_request)
        response = self.decoding_request(b_response)
        assert response.get('data') == invalid_data

    def test_code_invalid_request(self, invalid_request, invalid_code):
        c_request = self.encoding_request(invalid_request)
        b_response = handle_default_request(c_request)
        response = self.decoding_request(b_response)
        assert response.get('code') == invalid_code
