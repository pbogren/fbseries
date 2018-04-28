"""Set up package."""
from os.path import basename
from os.path import splitext
from glob import glob

from setuptools import find_packages
from setuptools import setup

setup(
    name='fbseries',
    version='0.1.0',
    author='Patrik Bogren',
    description='A simple gui program for managing a football series table.',
    license='Apache 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires=">=3.6",
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    entry_points={
        'gui_scripts': [
            'fbseries = fbseries.__main__:main',
        ]
    }
)
