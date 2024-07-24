"""Types for the body of Experimenter attributes.

Defines the body of Experimenter classes, like
ActionExperimenter or InstructionExperimenter
"""

from enum import IntEnum

from pyof.foundation.basic_types import Pad, UBInt8, UBInt16, UBInt32
from pyof.v0x04.common.action import ActionExperimenter


class NoviActionType(IntEnum):
    """Noviflow custom actions."""

    # Set BFD
    NOVI_ACTION_SET_BFD_DATA = 4

    # Push INT
    NOVI_ACTION_PUSH_INT = 12

    # Modify INT
    NOVI_ACTION_ADD_INT_METADATA = 13

    # Pop INT
    NOVI_ACTION_POP_INT = 14

    # Send INT report
    NOVI_ACTION_SEND_REPORT = 15


class ActionExperimenterNoviflow(ActionExperimenter):
    """Base class Noviflow's ActionExperimenter."""

    customer = UBInt8()
    reserved = UBInt8()
    novi_action_type = UBInt16(enum_ref=NoviActionType)

    _allowed_ids = (0xFF000002,)
    _allowed_novi = ()

    def __init__(self, length=16, customer=0xFF, reserved=0, novi_action_type=None):
        super().__init__(length=length, experimenter=0xFF000002)
        self.customer = customer
        self.reserved = reserved
        self.novi_action_type = novi_action_type

    @classmethod
    def get_allowed_novi(cls):
        """Get allowed novi"""
        return cls._allowed_novi

    @classmethod
    def get_subclass(cls, buff, offset):
        """Get subclass"""
        novi_action = UBInt16(enum_ref=NoviActionType)
        novi_action.unpack(buff, offset=offset + 2)
        for novi_cls in ActionExperimenterNoviflow.__subclasses__():
            if novi_action.value in novi_cls.get_allowed_novi():
                return novi_cls
        return cls


class NoviActionSetBfdData(ActionExperimenterNoviflow):  # LOOK AT ME
    """Set the BFD data."""

    port_no = UBInt32()
    my_disc = UBInt32()
    interval = UBInt32()
    multiplier = UBInt8()
    keep_alive_timeout = UBInt8()
    pad = Pad(6)

    _allowed_novi = (NoviActionType.NOVI_ACTION_SET_BFD_DATA,)

    def __init__(
        self,
        port_no=None,
        my_disc=None,
        interval=None,
        multiplier=None,
        keep_alive_timeout=None,
    ):
        super().__init__(
            length=32,
            customer=0xFF,
            reserved=0,
            novi_action_type=NoviActionType.NOVI_ACTION_SET_BFD_DATA,
        )
        self.port_no = port_no
        self.my_disc = my_disc
        self.interval = interval
        self.multiplier = multiplier
        self.keep_alive_timeout = keep_alive_timeout


class NoviActionPushInt(ActionExperimenterNoviflow):
    """Push INT action."""

    pad = Pad(4)

    _allowed_novi = (NoviActionType.NOVI_ACTION_PUSH_INT,)

    def __init__(self):
        super().__init__(
            customer=0xFF,
            reserved=0,
            novi_action_type=NoviActionType.NOVI_ACTION_PUSH_INT,
        )


class NoviActionAddIntMetadata(ActionExperimenterNoviflow):
    """Add INT metadata action."""

    pad = Pad(4)

    _allowed_novi = (NoviActionType.NOVI_ACTION_ADD_INT_METADATA,)

    def __init__(self):
        super().__init__(
            customer=0xFF,
            reserved=0,
            novi_action_type=NoviActionType.NOVI_ACTION_ADD_INT_METADATA,
        )


class NoviActionPopInt(ActionExperimenterNoviflow):
    """Pop INT action."""

    pad = Pad(4)

    _allowed_novi = (NoviActionType.NOVI_ACTION_POP_INT,)

    def __init__(self):
        super().__init__(
            customer=0xFF,
            reserved=0,
            novi_action_type=NoviActionType.NOVI_ACTION_POP_INT,
        )


class NoviActionSendReport(ActionExperimenterNoviflow):
    """Pop INT action."""

    pad = Pad(4)

    _allowed_novi = (NoviActionType.NOVI_ACTION_SEND_REPORT,)

    def __init__(self):
        super().__init__(
            customer=0xFF,
            reserved=0,
            novi_action_type=NoviActionType.NOVI_ACTION_SEND_REPORT,
        )
