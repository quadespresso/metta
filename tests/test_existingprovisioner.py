"""

Tests on the existing provisioner


"""

from mirantis.testing.mtt_dummy.plugins.client import DummyClientPlugin
from mirantis.testing.mtt.plugins.existing import ExistingBackendProvisionerPlugin
import mirantis.testing.mtt_dummy as mtt_dummy
import mirantis.testing.mtt as mtt
import logging
import pytest

logger = logging.getLogger(__file__)

# import the mtt core
# we use plugins from these two packages

# we import these only for assert isinstance checks


@pytest.fixture()
def existing_config():
    """ config Dict for the existing backend provisioner plugin """
    return {
        'provisioner': {
            'plugin_id': mtt.MTT_EXISTING_PROVISIONER_PLUGIN_ID,
            'outputs': {
                'main': {
                    "one": 1
                }
            },
            'clients': {
                'main': {
                    'plugin_id': mtt_dummy.MTT_PLUGIN_ID_DUMMY
                }
            }
        }
    }


@pytest.fixture()
def config(existing_config):
    """ Create a common Config """
    conf = mtt.new_config()
    conf.add_source(mtt.SOURCE_DICT).set_data(existing_config)

    return conf


@pytest.fixture()
def provisioner(config):
    """ Create provisioner as defined by config """
    provisioner = mtt.new_provisioner_from_config(config, 'existing')
    provisioner.prepare()
    return provisioner


def test_provisioner_sanit(provisioner):
    """ make sure that our provisioner is good """
    assert isinstance(provisioner, ExistingBackendProvisionerPlugin)


def test_existing_outputs(existing_config, provisioner):
    """ test that the existing provisioner handles programmed outputs """
    assert provisioner.output(
        'main') == existing_config['provisioner']['outputs']['main']


def test_existing_clients(existing_config, provisioner):
    """ test that the existing provisioner handles programmed outputs """

    client_main = provisioner.get_client('main')
    assert isinstance(client_main, DummyClientPlugin)
