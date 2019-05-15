Pyle
====

Use Python for sed or perl-like shell scripts
---------------------------------------------

Pyle makes it easy to use Python as a replacement for command line tools such as `sed` or `perl`.

To print the first 20 characters of each line of a file:

    cat README.md | pyle -e "line[:20]"

or:

    pyle -e "line[:20]" README.md

List all `/tmp/` files with a filename with an even length:

    ls /tmp/ | pyle -e "sh.ls('-l', line) if len(line) % 2 == 0 else None"

Perform an in-place string substitution, overwriting the original file with the updated file:

    pyle -ie "re.sub(r'alien(s|)?', r'ghost\1', line)" TextAboutAliens.md

The special variable`line` is the current line (if the input is multiple lines, the pyle expression is executed once per line). The variable `words` is the current line split by whitespace. To print just the URLs in an Apache access log (the seventh "word" in the line):

    tail access_log | pyle -e "words[6]"

Print the SHA 256 sum of each `*.py` file in the current directory:

    ls *.py | pyle -m hashlib -e "'%s %s' % (hashlib.sha256(line).hexdigest(), line)"
    348e4a65e24bab4eed8e2bbe6f4c8176ddec60051d1918eea38b34b1103a8af6 pyle.py
    b28c7f73e6df990a96cfb724be1d673c2d3c43f68d4b6c06d8e5a9b29e5d12cb pyle_test.py

If your expression returns a list or a tuple, the items will be printed joined by spaces. With that in mind we can simplify the above example:

    ls *.py | pyle -m hashlib -e "(hashlib.sha256(line).hexdigest(), line)"
    348e4a65e24bab4eed8e2bbe6f4c8176ddec60051d1918eea38b34b1103a8af6 pyle.py
    b28c7f73e6df990a96cfb724be1d673c2d3c43f68d4b6c06d8e5a9b29e5d12cb pyle_test.py

Print the first five lines of each file with file names and line numbers:

    pyle -e "'%-15s:%04d %s' % (filename, 1 + num, line) if num < 5 else None" *.py

You can also specify multiple expressions by repeating the `-e` option.  Just
like in `sed` each expression acts on `line` (and `words`, etc.) as modified by
the previous expression. E.g. replace a letter in the first five words of a file:

    pyle -e "words[:5]" -e "re.sub('A', 'B', line)" README.md

The idea for Pyle is based on Graham Fawcett's [PyLine](http://code.activestate.com/recipes/437932-pyle-a-grep-like-sed-like-command-line-tool/). Pyle is generally compatible with PyLine but requires a `-e` before the evaluation statement.

Pyle imports the [sh](https://github.com/amoffat/sh) module by default, which enables easy shell command execution.

## Installation ##

    pip install pyle

## Why Pyle? ##

Some of us are just simply awful at remembering the `sed`, `perl` or even `bash` syntax but feel right at home with Python. Python code is often a little more verbose but what good is saving characters if you can't remember what they do?

Here's an example of `sed` vs `pyle`. This isn't a very good `sed` expression, admittedly, but the people who will find Pyle useful are not `sed` experts.

To change home directories from `/var/X` to `/home/X` with sed:

    sed 's/^\(\([^:]*:\)\{5\}\)\/var\/\(.*\)/\1\/home\/\3/g' /etc/passwd

With Pyle:

    pyle -e "re.sub(r'^(([^:]*:){5})/var/(.*)', r'\1/home/\3', line)" /etc/passwd

If you find the Python code more readable, Pyle is for you.

## Documentation ##

This file and `pyle --help`.

## License ##

Free to use and modify under the terms of the BSD open source license.
