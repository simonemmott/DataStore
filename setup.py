import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='dictdiff',
    version='0.0.2',
    author_email='simon.emmott@yahoo.co.uk',
    author='Simon Emmott',
    description='Utility to calcualte the difference between two dicts',
    packages=['dictdiff',],
    long_description=read('README.md'),
    install_requires=[
        gti_spe_lib_json_model
    ],
)