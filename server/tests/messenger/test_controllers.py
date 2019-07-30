import pytest
from datetime import datetime

from messenger.controllers import send_message


@pytest.fixture
def expected_action():
    return 'send'


@pytest.fixture
def expected_code():
    return 200


@pytest.fixture
def expected_data():
    return 'Some data'


@pytest.fixture
def initial_request(expected_action, expected_data):
    return {
        'action': expected_action,
        'time': datetime.now().timestamp(),
        'data': expected_data
    }


def test_action_send_message(initial_request, expected_action):
    actual_response = send_message(initial_request)
    assert actual_response.get('action') == expected_action


def test_code_send_message(initial_request, expected_code):
    actual_response = send_message(initial_request)
    assert actual_response.get('code') == expected_code


def test_data_send_message(initial_request, expected_data):
    actual_response = send_message(initial_request)
    assert actual_response.get('data') == expected_data
