from distutils.core import setup

setup(name='pyle',
      version='0.3',
      description='Use Python for shell one-liners.',
      author='Alexander Ljungberg',
      author_email='aljungberg@slevenbits.com',
      url='https://github.com/aljungberg/pyle',
      py_modules=['pyle', 'pyle_test'],
      scripts=['pyle'],
      keywords=["shell"],
      classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
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
such as ``sed`` or ``perl``. For instance, to perform an in-place string
substitution, overwriting the original file with the updated file, you
might do:

::

    pyle -ie "re.sub(r'alien(s|)?', r'ghost\1', line)" TextAboutAliens.md

To print the first 20 characters of each line of a file:

::

    cat README.md | pyle -e "line[:20]"

or:

::

    pyle -e "line[:20]" README.md

In addition to ``line``, a list called ``words`` is also available which
is the current line split by whitespace. To print just the URLs in an
Apache access log (the seventh "word" in the line):

::

    tail access_log | pyle -e "words[6]"

Print the SHA 256 sum of each ``*.py`` file in the current directory:

::

    $ ls *.py | pyle -m hashlib -e "'%s %s' % (hashlib.sha256(line).hexdigest(), line)"
    348e4a65e24bab4eed8e2bbe6f4c8176ddec60051d1918eea38b34b1103a8af6 pyle.py
    b28c7f73e6df990a96cfb724be1d673c2d3c43f68d4b6c06d8e5a9b29e5d12cb pyle_test.py

If your expression returns a list or a tuple, the items will be printed
joined by spaces. With that in mind we can simplify the above example:

::

    $ ls *.py | pyle -m hashlib -e "(hashlib.sha256(line).hexdigest(), line)"
    348e4a65e24bab4eed8e2bbe6f4c8176ddec60051d1918eea38b34b1103a8af6 pyle.py
    b28c7f73e6df990a96cfb724be1d673c2d3c43f68d4b6c06d8e5a9b29e5d12cb pyle_test.py

Print the first five lines of each file with filenames and line numbers:

::

    $ pyle -e "'%-15s:%04d %s' % (filename, 1 + num, line) if num < 5 else None" *.py

The idea for Pyle is based on Graham Fawcett's
`PyLine <http://code.activestate.com/recipes/437932-pyle-a-grep-like-sed-like-command-line-tool/>`_.
Pyle is mostly compatible with PyLine but requires a ``-e`` before the
evaluation statement.
""",
      install_requires=[
        'argparse >= 1.2.1',
        'sh >= 1.0.9',
      ],

      )
