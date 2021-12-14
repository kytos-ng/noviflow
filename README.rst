Overview
========
Implement Noviflow-specific features

Requirements
============

This NApps depends on `kytos/of_core` and OpenFlow 1.3.

Supported Features
==================

The following `OFPAT_EXPERIMENTER` custom action types are supported:

  .. code-block:: python

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
