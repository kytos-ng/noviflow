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

from napps.amlight.noviflow.pyof.v0x04.action import (
    NoviActionSetBfdData as OFNoviActionSetBfdData,
    NoviActionPushInt as OFNoviActionPushInt,
    NoviActionAddIntMetadata as OFNoviActionAddIntMetadata,
    NoviActionPopInt as OFNoviActionPopInt,
    NoviActionSendReport as OFNoviActionSendReport,
    NoviActionType,
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

    def test_noviaction_experimenter_pack_unpack(self):
        """Test NoviAction* experimenter pack and unpack."""

        values = [
            (
                OFNoviActionPopInt,
                NoviActionType.NOVI_ACTION_POP_INT,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0e\x00\x00\x00\x00",
            ),
            (
                OFNoviActionPushInt,
                NoviActionType.NOVI_ACTION_PUSH_INT,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0c\x00\x00\x00\x00",
            ),
            (
                OFNoviActionAddIntMetadata,
                NoviActionType.NOVI_ACTION_ADD_INT_METADATA,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0d\x00\x00\x00\x00",
            ),
            (
                OFNoviActionSendReport,
                NoviActionType.NOVI_ACTION_SEND_REPORT,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0f\x00\x00\x00\x00",
            ),
        ]

        for action_class, action_type_val, expected_bytes in values:
            with self.subTest(
                action_class=action_class,
                action_type_val=action_type_val,
                expected_bytes=expected_bytes,
            ):
                action = action_class()
                packed = action.pack()

                assert packed == expected_bytes
                raw = expected_bytes

                unpacked = action_class()
                unpacked.unpack(raw)
                assert unpacked.customer.value == 0xFF
                assert unpacked.reserved.value == 0
                assert unpacked.novi_action_type.value == action_type_val.value

    def test_noviaction_set_bfd_data(self):
        """Test NoviActionSetBfdData experimenter pack and unpack."""

        port_no = 2
        my_disc = 1
        interval = 5
        multiplier = 3
        keep_alive_timeout = 15

        action = OFNoviActionSetBfdData(
            port_no=port_no,
            my_disc=my_disc,
            interval=interval,
            multiplier=multiplier,
            keep_alive_timeout=keep_alive_timeout,
        )
        packed = action.pack()

        unpacked = OFNoviActionSetBfdData()
        unpacked.unpack(packed)
        assert unpacked.customer.value == 0xFF
        assert unpacked.reserved.value == 0
        assert (
            unpacked.novi_action_type.value
            == NoviActionType.NOVI_ACTION_SET_BFD_DATA.value
        )
        assert unpacked.port_no == port_no
        assert unpacked.my_disc == my_disc
        assert unpacked.interval == interval
        assert unpacked.multiplier == multiplier
        assert unpacked.keep_alive_timeout == keep_alive_timeout
