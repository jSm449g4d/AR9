#9th

"""
#how to use
###Install
pip install git+https://github.com/jSm449g4d/AR9

###Uninstall
pip uninstall AR9
"""

from setuptools import setup,find_packages
from codecs import open
from os import path

setup(name='AR9',
      version='0.0.8',
      description='Distribution test',
      author='',
      author_email='',
      packages=find_packages(),
      url='',
      py_modules=['ARutil','ARSLR'],
      install_requires=['certifi','urllib3','beautifulsoup4'],
     )
