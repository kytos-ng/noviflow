"""Test Main methods."""
from unittest import TestCase
from unittest.mock import patch

from kytos.lib.helpers import (
    get_controller_mock,
    get_switch_mock,
)


# pylint: disable=protected-access, too-many-public-methods
class TestMain(TestCase):
    """Tests for the Main class."""

    def setUp(self):
        patch("kytos.core.helpers.run_on_thread", lambda x: x).start()
        # pylint: disable=import-outside-toplevel
        from napps.amlight.noviflow.main import Main

        self.addCleanup(patch.stopall)

        controller = get_controller_mock()
        self.switch_01 = get_switch_mock("00:00:00:00:00:00:00:01", 0x04)
        self.switch_01.is_enabled.return_value = True
        self.switch_01.flows = []

        self.switch_02 = get_switch_mock("00:00:00:00:00:00:00:02", 0x04)
        self.switch_02.is_enabled.return_value = False
        self.switch_02.flows = []

        controller.switches = {
            "00:00:00:00:00:00:00:01": self.switch_01,
            "00:00:00:00:00:00:00:02": self.switch_02,
        }

        self.napp = Main(controller)

    def test_pass(self):
        """Test pass."""
        pass
