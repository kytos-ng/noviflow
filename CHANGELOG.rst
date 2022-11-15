#########
Changelog
#########
All notable changes to the noviflow NApp will be documented in this file.

[UNRELEASED] - Under development
********************************
Added
=====

Changed
=======

Deprecated
==========

Removed
=======

Fixed
=====
- Fixed Action object has no attribute 'as_dict'
- Hooked ``ActionExperimenter`` subclasses to be deserialized on of_core

Security
========

[2022.1.0] - 2022-02-08
***********************

Added
=====
- Added support to NoviFlow OpenFlow custom Experimenter actions to enable BFD and INT
- Enhanced and standardized setup.py `install_requires` to install pinned dependencies
