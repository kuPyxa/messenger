from settings import INSTALLED_APPS


def test_settings():
    assert isinstance(INSTALLED_APPS, list)
