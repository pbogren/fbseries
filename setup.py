from setuptools import setup

setup(
    name='fbseries',
    version='0.1.0',
    author='Patrik Bogren',
    description='A simple gui program for managing a football series table.',
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'fbseries=fbseries.__main__:main',
        ]
    }
)
