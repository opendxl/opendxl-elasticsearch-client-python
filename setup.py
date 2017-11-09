import os

from setuptools import setup
import distutils.command.sdist

import setuptools.command.sdist

# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

version_info = {}
cwd=os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, "dxlelasticsearchclient", "_version.py")) as f:
    exec(f.read(), version_info)

dist = setup(
    # Package name:
    name="dxlelasticsearchclient",

    # Version number:
    version=version_info["__version__"],

    # Requirements
    install_requires=[
        "dxlbootstrap>=0.1.3",
        "dxlclient",
        "elasticsearch>=5.0.0,<6.0.0"
    ],

    # Package author details:
    author="McAfee LLC",

    # License
    license="Apache License 2.0",

    # Keywords
    keywords=['opendxl', 'dxl', 'mcafee', 'client', 'elasticsearch'],

    # Packages
    packages=[
        "dxlelasticsearchclient",
        "dxlelasticsearchclient._config",
        "dxlelasticsearchclient._config.sample"],

    package_data={
        "dxlelasticsearchclient._config.sample" : ['*']},

    # Details
    url="http://www.mcafee.com",

    description="Elasticsearch DXL Python client library",

    long_description=open('README').read(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
)
