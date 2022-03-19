
from setuptools import setup

setup(
    name = 'sheeticks', # while installing pacakge, e.g., matplotlib...
    version = '0.0.1',
    description = 'Shop Khata Management.',
    long_description = open('Readme.txt').read(),
    url = 'https://pypi.org/user/imvickykumar999/',
    author = 'Vicky Kumar',
    keywords = ['account', 'khata', 'class',
     'ideationology', 'google', 'sheet', 'worksheet', 'csv'],
    packages = ['khata', 'bank'], # while importing package, e.g., pyplot...
)

# python setup.py sdist
# pip install twine
# twine upload dist/*
