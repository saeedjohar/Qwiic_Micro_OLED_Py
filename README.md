# Qwiic_Micro_OLED_Py
Python package for the qwiic Micro OLED board


## Installation
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```
  $ python setup.py install
```

To build a package for use with pip:
```
  $ python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```
  cd dist
  pip install sparkfun_micro_oled-0.0.7.tar.gz