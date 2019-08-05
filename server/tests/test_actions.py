import pytest
from actions import get_server_actions, resolve


@pytest.fixture
def action_name():
    return 'test_action'


@pytest.fixture
def controller_name():
    return 'test_controller'


@pytest.fixture
def initial_actions(action_name, controller_name):
    return [{'action': action_name, 'controller': controller_name}]


def test_get_server_actions():
    assert isinstance(get_server_actions(), list)


def test_resolve(initial_actions, action_name, controller_name):
    resolved = resolve(action_name, initial_actions)
    assert resolved == controller_name
