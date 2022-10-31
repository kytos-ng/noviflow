"""Main module of amlight/noviflow Kytos Network Application.

Implement Noviflow-specific features
"""

from napps.amlight.noviflow.of_core.v0x04.action import (
    NoviActionAddIntMetadata,
    NoviActionPopInt,
    NoviActionPushInt,
    NoviActionSendReport,
    NoviActionSetBfdData,
    NoviActionAddIntMetadata as OFNoviActionAddIntMetadata,
    NoviActionPopInt as OFNoviActionPopInt,
    NoviActionPushInt as OFNoviActionPushInt,
    NoviActionSendReport as OFNoviActionSendReport,
    NoviActionSetBfdData as OFNoviActionSetBfdData,
)
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
        self.NOVIFLOW_ACTIONS = {
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

    def register_actions(self):
        """Add new actions to kytos/of_core."""
        for name, action in self.NOVIFLOW_ACTIONS.items():
            Action.add_action_class(name, action)
