import re
from setuptools import find_packages, setup

with open('rubika/__init__.py', 'r') as f:
    version = re.search(r'__version__\s*=\s*\'(\S+)\'', f.read()).group(1)


setup(
    name='rubika',
    version=version,
    url='https://github.com/IRMilad/rubika',
    description='rubika client for python 3',
    python_requires='>=3.7',
    packages=find_packages(exclude=['rubika*']),
    install_requires=['aiohttp', 'pycryptodome'],
    extras_require={
        'opencv-python': ['opencv-python']
    }
)
