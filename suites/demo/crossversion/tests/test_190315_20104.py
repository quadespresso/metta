"""

Test that some clients work

"""

import logging
import pytest

from . import EnvManager, TestBase

ENVIRONMENT = "190315-20104"
""" This test suite will run tests in a single environment, which will use this name """

logger = logging.getLogger(ENVIRONMENT)

# -- FIXTURES ------------------------------------------------------------

# PyTest fixtures don't work without redefining outer names
# pylint: disable=redefined-outer-name


@pytest.fixture(scope="module")
def env_manager():
    """get an instance of the EnvManager class"""
    return EnvManager(ENVIRONMENT)


@pytest.fixture(scope="module")
def environment_before(env_manager):
    """Make sure that we have an environment in scope"""
    environment = env_manager.get_env_in_state(state="before")
    env_manager.install(environment)
    return environment
    # we don't yield here, as we will expect your test case to also use the environment-after
    # fixture which will be responsible for teardown.


@pytest.fixture(scope="module")
def environment_after(env_manager):
    """Make sure that we have an environment in scope"""
    environment = env_manager.get_env_in_state(state="after")
    env_manager.upgrade(environment)
    yield environment
    # on teardown, destroy the env resources (pytest behaviour)
    env_manager.destroy(environment)


# -- TEST FUNCTIONS -------------------------------------------------------


class TestUpgrade(TestBase):
    """Test suite for the cross-version upgrade"""

    __test__ = True

    def test_health_check_before(self, environment_before):
        """Run health checks on the BEFORE state."""
        self.health(environment_before)

    def test_health_check_after(self, environment_after):
        """Run health checks on the AFTER state."""
        self.health(environment_after)
