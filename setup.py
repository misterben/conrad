#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import libconrad

setup(name = 'libconrad',
      description = 'Static site generator',
      long_description = read('README.rst'),
      license = 'BSD',
      version = libconrad.__version__,
      author = 'Alexander Solovyov',
      author_email = 'alexander@solovyov.net',
      url = 'http://piranha.org.ua/libconrad/',
      install_requires = ['Jinja2', 'smartypants'],
      packages = ['libconrad', 'libconrad.template'],

      entry_points = {
        'console_scripts': ['libconrad = libconrad:main']
        },

      classifiers = [
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        ],
      platforms='any',
      )
