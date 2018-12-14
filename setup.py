import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


# Package meta-data.
NAME = 'update_repo'
DESCRIPTION = 'repository updater'
URL = 'https://github.com/Bno93/repo-update.git'
EMAIL = 'benno.schweikert@googlemail.com'
AUTHOR = 'Benno Schweikert'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'yattag'
    'wxPython'
]

# What packages are optional?
EXTRAS = {

}


here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    desciption=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_required=REQUIRED,
    extra_require=EXTRAS,
    include_package_data=True,
)