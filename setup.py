# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements= f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tmtransfers',
    version='0.1.0',
    install_requires=requirements,
    description='Script to web scrape league transfer data from Transfermarkt',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Eric M. Ordonez',
    author_email='',
    url='https://github.com/emordonez/transfermarkt-transfers',
    license=license,
    packages=find_packages(exclude=['data', 'tests'])
)
