"""Test Main methods."""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from napps.amlight.noviflow.of_core.v0x04.action import (
    NoviActionAddIntMetadata,
    NoviActionPopInt,
    NoviActionPushInt,
    NoviActionSendReport,
    NoviActionSetBfdData,
)
from napps.amlight.noviflow.pyof.v0x04.action import (
    NoviActionAddIntMetadata as OFNoviActionAddIntMetadata,
)
from napps.amlight.noviflow.pyof.v0x04.action import (
    NoviActionPopInt as OFNoviActionPopInt,
)
from napps.amlight.noviflow.pyof.v0x04.action import (
    NoviActionPushInt as OFNoviActionPushInt,
)
from napps.amlight.noviflow.pyof.v0x04.action import (
    NoviActionSendReport as OFNoviActionSendReport,
)
from napps.amlight.noviflow.pyof.v0x04.action import (
    NoviActionSetBfdData as OFNoviActionSetBfdData,
)
from napps.amlight.noviflow.pyof.v0x04.action import NoviActionType
from napps.kytos.of_core.v0x04.flow import Flow as Flow04
from pyof.foundation.basic_types import UBInt8, UBInt32

from kytos.lib.helpers import get_controller_mock, get_switch_mock


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

    def test_execute_register_actions(self) -> None:
        """Test register_actions is executed."""
        mock = MagicMock()
        self.napp.register_actions = mock()
        self.napp.execute()
        assert mock.call_count == 1

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
                NoviActionPopInt,
            ),
            (
                OFNoviActionPushInt,
                NoviActionType.NOVI_ACTION_PUSH_INT,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0c\x00\x00\x00\x00",
                NoviActionPushInt,
            ),
            (
                OFNoviActionAddIntMetadata,
                NoviActionType.NOVI_ACTION_ADD_INT_METADATA,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0d\x00\x00\x00\x00",
                NoviActionAddIntMetadata,
            ),
            (
                OFNoviActionSendReport,
                NoviActionType.NOVI_ACTION_SEND_REPORT,
                b"\xff\xff\x00\x10\xff\x00\x00\x02\xff\x00\x00\x0f\x00\x00\x00\x00",
                NoviActionSendReport,
            ),
        ]

        for action_class, action_type_val, expected_bytes, novi_class in values:
            with self.subTest(
                action_class=action_class,
                action_type_val=action_type_val,
                expected_bytes=expected_bytes,
                novi_class=novi_class,
            ):
                action = action_class()
                packed = action.pack()

                assert packed == expected_bytes
                raw = expected_bytes

                unpacked = action_class()
                unpacked.unpack(raw)
                assert unpacked.customer == 0xFF
                assert unpacked.reserved == 0
                assert unpacked.novi_action_type.value == action_type_val.value

                assert isinstance(novi_class.from_of_action(action), novi_class)
                as_of_action = novi_class().as_of_action()
                assert isinstance(as_of_action, action_class)
                assert as_of_action.customer == 0xFF
                assert as_of_action.reserved == 0
                assert as_of_action.novi_action_type.value == action_type_val.value

    def test_noviaction_set_bfd_data(self):
        """Test NoviActionSetBfdData experimenter pack and unpack."""

        port_no = UBInt32(2)
        my_disc = UBInt32(1)
        interval = UBInt32(5)
        multiplier = UBInt8(3)
        keep_alive_timeout = UBInt8(15)

        action = OFNoviActionSetBfdData(
            port_no=port_no,
            my_disc=my_disc,
            interval=interval,
            multiplier=multiplier,
            keep_alive_timeout=keep_alive_timeout,
        )
        assert action.customer == 0xFF
        assert action.reserved == 0
        assert action.port_no == 2
        assert action.my_disc == 1
        assert action.interval == 5
        assert action.multiplier == 3
        assert action.keep_alive_timeout == 15

        packed = action.pack()
        expected = b"\xff\xff\x00 \xff\x00\x00\x02\xff\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x05\x03\x0f\x00\x00\x00\x00\x00\x00"
        assert packed == expected
        assert len(packed) == 32

        unpacked = OFNoviActionSetBfdData()
        unpacked.unpack(packed)
        assert unpacked.customer == 0xFF
        assert unpacked.reserved == 0
        assert (
            unpacked.novi_action_type.value
            == NoviActionType.NOVI_ACTION_SET_BFD_DATA.value
        )
        assert unpacked.port_no == port_no
        assert unpacked.my_disc == my_disc
        assert unpacked.interval == interval
        assert unpacked.multiplier == multiplier
        assert unpacked.keep_alive_timeout == keep_alive_timeout

        novi_class = NoviActionSetBfdData(
            port_no=port_no,
            my_disc=my_disc,
            interval=interval,
            multiplier=multiplier,
            keep_alive_timeout=keep_alive_timeout,
        )
        assert isinstance(novi_class.from_of_action(action), NoviActionSetBfdData)
        as_of_action = novi_class.as_of_action()
        assert isinstance(as_of_action, OFNoviActionSetBfdData)
        assert as_of_action.customer == 0xFF
        assert as_of_action.reserved == 0
        assert (
            as_of_action.novi_action_type.value
            == NoviActionType.NOVI_ACTION_SET_BFD_DATA.value
        )
        assert as_of_action.port_no == port_no
        assert as_of_action.my_disc == my_disc
        assert as_of_action.interval == interval
        assert as_of_action.multiplier == multiplier
        assert as_of_action.keep_alive_timeout == keep_alive_timeout

    def test_noviflow_actions_dict(self) -> None:
        """Test NOVIFLOW_ACTIONS dict."""
        expected_keys = [
            "set_bfd",
            "push_int",
            "add_int_metadata",
            "pop_int",
            "send_report",
            NoviActionSetBfdData,
            NoviActionPushInt,
            NoviActionAddIntMetadata,
            NoviActionPopInt,
            NoviActionSendReport,
        ]
        assert expected_keys == list(self.napp.NOVIFLOW_ACTIONS.keys())
