Pyle
====

Use Python for sed or perl-like shell scripts
---------------------------------------------

Pyle makes it easy to use Python as a replacement for command line tools such as `sed` or `perl`. For instance, to perform an in-place string substitution, overwriting the original file with the updated file, you might do:

    pyle -ie "re.sub(r'alien(s|)?', r'ghost\1', line)" TextAboutAliens.md

To print the first 20 characters of each line of a file:

    cat README.md | pyle -e "line[:20]"

or:

    pyle -e "line[:20]" README.md

In addition to `line`, a list called `words` is also available which is the current line split by whitespace. To print just the URLs in an Apache access log (the seventh "word" in the line):

    tail access_log | pyle -e "words[6]"

Print the SHA 256 sum of each `*.py` file in the current directory:

    $ ls *.py | pyle -m hashlib -e "'%s %s' % (hashlib.sha256(line).hexdigest(), line)"
    348e4a65e24bab4eed8e2bbe6f4c8176ddec60051d1918eea38b34b1103a8af6 pyle.py
    b28c7f73e6df990a96cfb724be1d673c2d3c43f68d4b6c06d8e5a9b29e5d12cb pyle_test.py

If your expression returns a list or a tuple, the items will be printed joined by spaces. With that in mind we can simplify the above example:

    $ ls *.py | pyle -m hashlib -e "(hashlib.sha256(line).hexdigest(), line)"
    348e4a65e24bab4eed8e2bbe6f4c8176ddec60051d1918eea38b34b1103a8af6 pyle.py
    b28c7f73e6df990a96cfb724be1d673c2d3c43f68d4b6c06d8e5a9b29e5d12cb pyle_test.py

Print the first five lines of each file with filenames and line numbers:

    $ pyle -e "'%-15s:%04d %s' % (filename, 1 + num, line) if num < 5 else None" *.py

The idea for Pyle is based on Graham Fawcett's [PyLine](http://code.activestate.com/recipes/437932-pyle-a-grep-like-sed-like-command-line-tool/). Pyle is mostly compatible with PyLine but requires a `-e` before the evaluation statement.

## Installation ##

Download `pyle.py` and put it in your path. Give it the executable bit.

    sudo mv pyle.py /usr/local/bin/pyle
    sudo chmod +x /usr/local/bin/pyle

## Why Pyle? ##

Some of us are just simply awful at remembering the `sed`, `perl` or even `bash` syntax but feel right at home with Python. Python code is often a little more verbose but what good is saving characters if you can't remember what they do?

Here's an example of `sed` vs `pyle`. This isn't a very good `sed` expression, admittedly, but the people who will find Pyle useful are not `sed` experts.

To change home directories from `/var/X` to `/home/X`:

    sed 's/^\(\([^:]*:\)\{5\}\)\/var\/\(.*\)/\1\/home\/\3/g' /etc/passwd
    pyle -e "re.sub(r'^(([^:]*:){5})/var/(.*)', r'\1/home/\3', line)" /etc/passwd

If you find the Python code more readable, Pyle is for you.

## Documentation ##

This file and `pyle --help`.

## License ##

Free to use and modify under the terms of the BSD open source license.
