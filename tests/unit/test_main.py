"""Test Main methods."""
from unittest import TestCase
from unittest.mock import patch
from napps.kytos.of_core.v0x04.flow import Flow as Flow04
from napps.amlight.noviflow.of_core.v0x04.action import (
    NoviActionPushInt,
    NoviActionSetBfdData,
    NoviActionAddIntMetadata,
    NoviActionPopInt,
    NoviActionSendReport,
)

from kytos.lib.helpers import (
    get_controller_mock,
    get_switch_mock,
)


class TestMain(TestCase):
    """Tests for the Main class."""

    def setUp(self):
        patch("kytos.core.helpers.run_on_thread", lambda x: x).start()
        # pylint: disable=import-outside-toplevel
        from napps.amlight.noviflow.main import Main

        self.addCleanup(patch.stopall)

        controller = get_controller_mock()
        self.napp = Main(controller)
        self.napp.register_actions()
        self.mock_switch = get_switch_mock("00:00:00:00:00:00:00:01", 0x04)

    def test_create_noviactions(self):
        """Test creating NoviAction classes from a Flow04."""

        some_match = {"dl_src": "11:22:33:44:55:66"}
        payload_classes = [
            (
                {
                    "switch": self.mock_switch.id,
                    "match": some_match,
                    "actions": [
                        {
                            "action_type": "set_bfd",
                            "port_no": 1,
                            "my_disc": 1,
                            "interval": 5,
                            "multiplier": 3,
                            "keep_alive_timeout": 15,
                        }
                    ],
                },
                NoviActionSetBfdData,
            ),
            (
                {
                    "switch": self.mock_switch.id,
                    "match": some_match,
                    "actions": [{"action_type": "push_int"}],
                },
                NoviActionPushInt,
            ),
            (
                {
                    "switch": self.mock_switch.id,
                    "match": some_match,
                    "actions": [{"action_type": "pop_int"}],
                },
                NoviActionPopInt,
            ),
            (
                {
                    "switch": self.mock_switch.id,
                    "match": some_match,
                    "actions": [{"action_type": "send_report"}],
                },
                NoviActionSendReport,
            ),
            (
                {
                    "switch": self.mock_switch.id,
                    "match": some_match,
                    "actions": [{"action_type": "add_int_metadata"}],
                },
                NoviActionAddIntMetadata,
            ),
        ]

        for payload, expected_class in payload_classes:
            with self.subTest(payload=payload, expected_class=expected_class):
                flow = Flow04.from_dict(payload, self.mock_switch)
                assert isinstance(flow.instructions[0].actions[0], expected_class)

    def test__eq__success_with_equal_flows(self):
        """Test success case to __eq__ override with equal flows."""

        flow_dict = {
            "switch": self.mock_switch.id,
            "table_id": 1,
            "match": {"dl_src": "11:22:33:44:55:66"},
            "priority": 2,
            "idle_timeout": 3,
            "hard_timeout": 4,
            "cookie": 5,
            "actions": [{"action_type": "push_int"}],
        }

        flow_1 = Flow04.from_dict(flow_dict, self.mock_switch)
        flow_2 = Flow04.from_dict(flow_dict, self.mock_switch)
        assert flow_1 == flow_2

    def test__eq__success_with_different_flows(self):
        """Test success case to __eq__ override with different flows."""

        flow_1_port_no = 1
        flow_dict_1 = {
            "switch": self.mock_switch.id,
            "table_id": 1,
            "match": {"dl_src": "11:22:33:44:55:66"},
            "actions": [
                {
                    "action_type": "set_bfd",
                    "port_no": flow_1_port_no,
                    "my_disc": 1,
                    "interval": 5,
                    "multiplier": 3,
                    "keep_alive_timeout": 15,
                }
            ],
        }

        flow_dict_2 = {
            "switch": self.mock_switch.id,
            "table_id": 1,
            "match": {"dl_src": "11:22:33:44:55:66"},
            "actions": [
                {
                    "action_type": "set_bfd",
                    "port_no": flow_1_port_no + 1,
                    "my_disc": 1,
                    "interval": 5,
                    "multiplier": 3,
                    "keep_alive_timeout": 15,
                }
            ],
        }

        flow_1 = Flow04.from_dict(flow_dict_1, self.mock_switch)
        flow_2 = Flow04.from_dict(flow_dict_2, self.mock_switch)
        assert flow_1 != flow_2
