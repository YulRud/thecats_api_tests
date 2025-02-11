import pytest
from util.logger_util import Logger

@pytest.fixture(scope='module')
def api_key():
    return 'live_Qc2yvxGD20H7cPuXf2TMWoxZmGT25UVZyPKHwR5vIlxLvmjLvx01PwXo8rXYu78O'


@pytest.fixture(scope='session')
def test_logger():
    fixture_logger = Logger(__name__).get_logger()
    fixture_logger.info('Loggin of test execution has started')

    yield fixture_logger

    fixture_logger.info('Logging of test execution has ended')
    fixture_logger = None