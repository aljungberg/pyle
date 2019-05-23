from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup

setup(
    name='pyle',
    version='0.4.1',
    description='Use Python for shell one-liners.',
    author='Alexander Ljungberg',
    author_email='aljungberg@slevenbits.com',
    url='https://github.com/aljungberg/pyle',
    license='BSD',
    py_modules=['pyle'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    scripts=['pyle'],
    test_suite='pyle_test',
    keywords=["shell"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Topic :: System :: Shells",
        "Topic :: System :: Systems Administration"
    ],
    long_description="""\
    Use Python for shell one-liners
    -------------------------------
    
    Pyle makes it easy to use Python as a replacement for command line tools
    such as ``sed`` or ``perl``. 
    
    See https://github.com/aljungberg/pyle for more information.
    """,
    long_description_content_type='text/markdown',
    install_requires=[
        'sh >= 1.12.14',
        'future >= 0.17.1',
    ],
)
