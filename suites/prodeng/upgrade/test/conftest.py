"""

PyTest fixtures for the upgrade test.

"""
import logging

import pytest

from mirantis.testing.metta.fixture import Fixtures
from mirantis.testing.metta.workload import METTA_PLUGIN_INTERFACE_ROLE_WORKLOAD
from mirantis.testing.metta_health.healthpoll_workload import (
    HealthPollWorkload,
    METTA_PLUGIN_ID_WORKLOAD_HEALTHPOLL,
)

logger = logging.getLogger("stability-conftest")

# impossible to chain pytest fixtures without using the same names
# pylint: disable=redefined-outer-name
# unused argument is their to force dependency hierarchy
# pylint: disable=unused-argument


@pytest.fixture(scope="session")
def workloads(environment) -> Fixtures:
    """Return a Fixtures set of workload plugins.

    These are the plugins that are meant to apply load
    to the cluster during the longevity test, and will
    not include the healthpolling workload.

    Returns:
    --------
    Fixtures list of workloads but without the healthpoller.
    """
    workload_fixtures = Fixtures()

    # Take any workload plugin other than the healthpoll plugin
    for fixture in environment.fixtures().filter(
        interfaces=[METTA_PLUGIN_INTERFACE_ROLE_WORKLOAD]
    ):
        if fixture.plugin_id == METTA_PLUGIN_ID_WORKLOAD_HEALTHPOLL:
            continue

        workload_fixtures.add(fixture)

    return workload_fixtures


@pytest.fixture(scope="module")
def healthpoller(environment) -> HealthPollWorkload:
    """Start a running health poll and return it."""
    healthpoll_workload = environment.fixtures().get_plugin(
        plugin_id=METTA_PLUGIN_ID_WORKLOAD_HEALTHPOLL
    )

    healthpoll_workload.prepare(environment.fixtures())
    healthpoll_workload.apply()

    yield healthpoll_workload

    healthpoll_workload.destroy()
