#!/usr/bin/env python
#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from setuptools import setup, find_packages

from telepathy import __version__, __author__, __licence__


requires = [
    'docopt',
    'rq',
    'redis',
    'rq-dashboard',
    'flask-restful',
    'Logbook',
    'rethinkdb']


def long_description():
    try:
        #with codecs.open(readme, encoding='utf8') as f:
        with open('readme.md') as f:
            return f.read()
    except IOError:
        return "failed to read README.md"


setup(
    name='telepathy',
    version=__version__,
    description='This plugin provides a RESTFul interface to intuition',
    author=__author__,
    author_email='xavier.bruhiere@gmail.com',
    packages=find_packages(),
    long_description=long_description(),
    license=__licence__,
    install_requires=requires,
    url="https://github.com/hackliff/intuition-plugins",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Distributed Computing',
    ],
    scripts=['app/telepathy'],
    data_files=[(os.path.expanduser('~/.intuition'), ['app/Procfile'])]
)
