import contextlib

import pytest

import dsi

capmanager = None


def called_from_pytest():
    return hasattr(dsi, "_dsi_called_from_pytest") and dsi._dsi_called_from_pytest


@contextlib.contextmanager
def disable_capture():
    if called_from_pytest() and capmanager:
        with capmanager.global_and_fixture_disabled():
            yield
    else:
        yield


@pytest.fixture(scope="session", autouse=True)
def set_pytest_flag():
    dsi._dsi_called_from_pytest = True
    yield
    del dsi._dsi_called_from_pytest


class DsiUtils:
    # @TODO: maybe do something useful here?
    pass


def pytest_configure(config):
    global capmanager
    capmanager = config.pluginmanager.getplugin('capturemanager')
    config._dsi = DsiUtils()
    config.pluginmanager.register(config._dsi)
