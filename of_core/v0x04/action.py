"""Of_core.v0x04.action"""

# pylint: disable=unused-argument


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
from napps.kytos.of_core.flow import ActionBase


class NoviActionSetBfdData(ActionBase):
    """Action with an BFD fields."""

    def __init__(self, port_no, my_disc, interval, multiplier, keep_alive_timeout):
        """Require BFD fields."""
        self.port_no = port_no
        self.my_disc = my_disc
        self.interval = interval
        self.multiplier = multiplier
        self.keep_alive_timeout = keep_alive_timeout
        self.action_type = "set_bfd"

    @classmethod
    def from_of_action(cls, of_action):
        """Return a high-level NoviActionSetBfdData instance from pyof."""
        return cls(
            port_no=of_action.port_no.value,
            my_disc=of_action.my_disc.value,
            interval=of_action.interval.value,
            multiplier=of_action.multiplier.value,
            keep_alive_timeout=of_action.keep_alive_timeout.value,
        )

    def as_of_action(self):
        """Return a pyof NoviActionSetBfdData instance."""
        return OFNoviActionSetBfdData(
            port_no=self.port_no,
            my_disc=self.my_disc,
            interval=self.interval,
            multiplier=self.multiplier,
            keep_alive_timeout=self.keep_alive_timeout,
        )


class NoviActionPushInt(ActionBase):
    """Action to push INT."""

    def __init__(self):
        self.action_type = "push_int"

    @classmethod
    def from_of_action(cls, of_action):
        """Return a high-level NoviActionPushInt instance from pyof."""
        return cls()

    def as_of_action(self):
        """Return a pyof NoviActionPushInt instance."""
        return OFNoviActionPushInt()


class NoviActionAddIntMetadata(ActionBase):
    """Action to add INT metadata."""

    def __init__(self, *args):
        self.action_type = "add_int_metadata"

    @classmethod
    def from_of_action(cls, of_action):
        """Return a high-level NoviActionAddIntMetadata instance from pyof."""
        return cls()

    def as_of_action(self):
        """Return a pyof NoviActionAddIntMetadata instance."""
        return OFNoviActionAddIntMetadata()


class NoviActionPopInt(ActionBase):
    """Action to pop INT."""

    def __init__(self, *args):
        self.action_type = "pop_int"

    @classmethod
    def from_of_action(cls, of_action):
        """Return a high-level NoviActionPopInt instance from pyof."""
        return cls()

    def as_of_action(self):
        """Return a pyof NoviActionPopInt instance."""
        return OFNoviActionPopInt()


class NoviActionSendReport(ActionBase):
    """Action to send INT report."""

    def __init__(self, *args):
        self.action_type = "send_report"

    @classmethod
    def from_of_action(cls, of_action):
        """Return a high-level NoviActionSendReport instance from pyof."""
        return cls()

    def as_of_action(self):
        """Return a pyof NoviActionSendReport instance."""
        return OFNoviActionSendReport()
