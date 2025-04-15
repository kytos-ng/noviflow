#########
Changelog
#########
All notable changes to the noviflow NApp will be documented in this file.

[UNRELEASED] - Under development
********************************

[2025.1.0] - 2025-04-14
***********************

No major changes since the last release.

[2024.1.0] - 2024-07-23
***********************

Changed
=======
- Updated python environment installation from 3.9 to 3.11

[2022.3.0] - 2022-12-15
***********************

Fixed
=====
- Fixed Action object has no attribute 'as_dict'
- Hooked ``ActionExperimenter`` subclasses to be deserialized on of_core

[2022.1.0] - 2022-02-08
***********************

Added
=====
- Added support to NoviFlow OpenFlow custom Experimenter actions to enable BFD and INT
- Enhanced and standardized setup.py `install_requires` to install pinned dependencies
