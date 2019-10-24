from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
from codecs import open
from os import path



here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

line = '= "UNKNOWN"'
for line in open(path.join(here, 'pycmap/__init__.py'), encoding='utf-8'):
    if line.startswith('__version__'):
        break
version = eval(line.split('=', 1)[1].strip())  # pylint: disable=eval-used


setup(
    name='pycmap',
    version=version,
    description='Simons CMAP API python client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/simonscmap/pycmap',
    author='Mohammad D. Ashkezari',
    author_email='mdehghan@uw.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='ocean oceanography data visualization satellite model in-situ remote sensing machine learning', 
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'numpy', 
        'pandas', 
        'scipy', 
        'bokeh', 
        'matplotlib', 
        'cmocean',
        'tqdm', 
        'folium', 
        'colorama',
        'plotly'
        ],
)
