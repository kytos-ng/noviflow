"""Main module of amlight/noviflow Kytos Network Application.

Implement Noviflow-specific features
"""

import struct
from typing import Optional, Type

from napps.amlight.noviflow.of_core.v0x04.action import (
    NoviActionAddIntMetadata,
    NoviActionPopInt,
    NoviActionPushInt,
    NoviActionSendReport,
    NoviActionSetBfdData,
)
from napps.amlight.noviflow.pyof.v0x04.action import ActionExperimenterNoviflow
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
from napps.amlight.noviflow.pyof.v0x04.action import NoviActionType as NType
from napps.kytos.of_core.v0x04.flow import Action

from kytos.core import KytosNApp


class Main(KytosNApp):
    """Main class of amlight/noviflow NApp.

    This class is the entry point for this NApp.
    """

    def setup(self):
        """Replace the '__init__' method for the KytosNApp subclass.

        The setup method is automatically called by the controller when your
        application is loaded.

        So, if you have any setup routine, insert it here.
        """
        self.noviflow_actions = {
            "set_bfd": NoviActionSetBfdData,
            "push_int": NoviActionPushInt,
            "add_int_metadata": NoviActionAddIntMetadata,
            "pop_int": NoviActionPopInt,
            "send_report": NoviActionSendReport,
            OFNoviActionSetBfdData: NoviActionSetBfdData,
            OFNoviActionPushInt: NoviActionPushInt,
            OFNoviActionAddIntMetadata: NoviActionAddIntMetadata,
            OFNoviActionPopInt: NoviActionPopInt,
            OFNoviActionSendReport: NoviActionSendReport,
        }

        self.noviflow_action_types = {
            NType.NOVI_ACTION_SET_BFD_DATA: NoviActionSetBfdData,
            NType.NOVI_ACTION_PUSH_INT.value: NoviActionPushInt,
            NType.NOVI_ACTION_ADD_INT_METADATA.value: NoviActionAddIntMetadata,
            NType.NOVI_ACTION_POP_INT: NoviActionPopInt,
            NType.NOVI_ACTION_SEND_REPORT: NoviActionSendReport,
        }

    def execute(self):
        """Run after the setup method execution.

        You can also use this method in loop mode if you add to the above setup
        method a line like the following example:

            self.execute_as_loop(30)  # 30-second interval.
        """
        self.register_actions()

    def shutdown(self):
        """Run when your NApp is unloaded.

        If you have some cleanup procedure, insert it here.
        """
        pass

    def get_experimenter_type(
        self,
        body: bytes
    ) -> Optional[Type[ActionExperimenterNoviflow]]:
        """Get ActionExperimenterNoviflow given an encoded action body."""
        try:
            (customer, _rsv, action_type) = struct.unpack("!BBH", body[:4])
            if customer != 0xff:
                return None
            return self.noviflow_action_types.get(action_type)
        except struct.error:
            return None

    def register_actions(self):
        """Add new actions to kytos/of_core."""
        for name, action in self.noviflow_actions.items():
            Action.add_action_class(name, action)
        exp = int(ActionExperimenterNoviflow().experimenter)
        Action.add_experimenter_classes(exp, self.get_experimenter_type)
