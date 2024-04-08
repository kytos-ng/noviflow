|Tag| |License| |Build| |Coverage| |Quality|

.. raw:: html

  <div align="center">
    <h1><code>amlight/noviflow</code></h1>

    <strong>NApp that implements Noviflow specific features </strong>
  </div>


Overview
========
Implement Noviflow-specific features

Installing
==========

To install this NApp, first, make sure to have the same venv activated as you have ``kytos`` installed on:

.. code:: shell

   $ git clone https://github.com/kytos-ng/noviflow.git
   $ cd noviflow
   $ python -m pip install --editable .

To install the kytos environment, please follow our
`development environment setup <https://github.com/kytos-ng/documentation/blob/master/tutorials/napps/development_environment_setup.rst>`_.

Requirements
============

This NApps depends on `kytos/of_core` and OpenFlow 1.3.

Supported Features
==================

The following ``OFPAT_EXPERIMENTER`` custom action types are supported:

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

.. TAGs

.. |Build| image:: https://scrutinizer-ci.com/g/kytos-ng/noviflow/badges/build.png?b=master
  :alt: Build status
.. |Coverage| image:: https://scrutinizer-ci.com/g/kytos-ng/noviflow/badges/coverage.png?b=master
  :alt: Code coverage
  :target: https://scrutinizer-ci.com/g/kytos-ng/noviflow/?branch=master
.. |Quality| image:: https://scrutinizer-ci.com/g/kytos-ng/noviflow/badges/quality-score.png?b=master
  :alt: Code-quality score
  :target: https://scrutinizer-ci.com/g/kytos-ng/noviflow/?branch=master
.. |Tag| image:: https://img.shields.io/github/tag/kytos-ng/noviflow.svg
   :target: https://github.com/kytos-ng/noviflow/tags
.. |License| image:: https://img.shields.io/github/license/kytos-ng/noviflow.svg
   :target: https://github.com/kytos-ng/noviflow/blob/master/LICENSE
