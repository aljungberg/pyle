#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Pyle allows you to use Python as a replacement for command line tools such
as `sed` or `perl`. It reads its standard input and evaluates each line with
the expression specified, outputting the results on standard out.
Optionally, it can operate on a list of filenames instead in which case each
file is read and processed in order.

The following variables are available in the global scope:

    * `line`:       the current input line being processed
    * `words`:      line split by whitespace
    * `num`:        line number
    * `filename`:   the name of the current file

The following modules are imported by default:

    * `re`:         Python regular expressions
    * `sh`:         the [`sh` module (formerly `pbs`)](https://pypi.python.org/pypi/sh)

The sh module makes it easy to run additional commands from within the expression.

"""

__version__ = "0.2"

import argparse
import cStringIO as StringIO
import re
import sh
import sys
import traceback

STANDARD_MODULES = {
    're': re,
    'sh': sh
}


def truncate_ellipsis(line, length=30):
    """Truncate a line to the specified length followed by ``...`` unless its shorter than length already."""

    l = len(line)
    return line if l < length else line[:length - 3] + "..."


def pyle_evaluate(expressions=None, modules=(), inplace=False, files=None, print_traceback=False):
    """The main method of pyle."""

    eval_globals = {}

    eval_globals.update(STANDARD_MODULES)

    for module_arg in modules or ():
        for module in module_arg.strip().split(","):
            module = module.strip()
            if module:
                eval_globals[module] = __import__(module)

    if not expressions:
        # Default 'do nothing' program
        expressions = ['line']

    files = files or ['-']
    eval_locals = {}
    for file in files:
        if file == '-':
            file = sys.stdin

        out_buf = sys.stdout if not inplace else StringIO.StringIO()

        out_line = None
        with (open(file, 'rb') if not hasattr(file, 'read') else file) as in_file:
            for num, line in enumerate(in_file.readlines()):
                was_whole_line = False
                if line[-1] == '\n':
                    was_whole_line = True
                    line = line[:-1]

                expr = ""
                try:
                    for expr in expressions:
                        words = [word.strip()
                                 for word in re.split(r'\s+', line)
                                 if word]
                        eval_locals.update({
                            'line': line, 'words': words,
                            'filename': in_file.name, 'num': num
                            })

                        out_line = eval(expr, eval_globals, eval_locals)

                        if out_line is None:
                            continue

                        # If the result is something list-like or iterable,
                        # output each item space separated.
                        if not isinstance(out_line, str) and not isinstance(out_line, unicode):
                            try:
                                out_line = u' '.join(unicode(part)
                                                     for part in out_line)
                            except:
                                # Guess it wasn't a list after all.
                                out_line = unicode(out_line)

                        line = out_line
                except Exception as e:
                    sys.stdout.flush()
                    sys.stderr.write("At %s:%d ('%s'): `%s`: %s\n" % (
                        in_file.name, num, truncate_ellipsis(line), expr, e))
                    if print_traceback:
                        traceback.print_exc(None, sys.stderr)
                else:
                    if out_line is None:
                        continue

                    out_line = out_line or u''
                    out_buf.write(out_line)
                    if was_whole_line:
                        out_buf.write('\n')
        if inplace:
            with open(file, 'wb') as out_file:
                out_file.write(out_buf.getvalue())
            out_buf.close()


def pyle(argv=None):
    """Execute pyle with the specified arguments, or sys.argv if no arguments specified."""

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-m", "--modules", dest="modules", action='append',
        help="import MODULE before evaluation. May be specified more than once.")
    parser.add_argument("-i", "--inplace", dest="inplace", action='store_true', default=False,
        help="edit files in place. When used with file name arguments, the files will be replaced by the output of the evaluation")
    parser.add_argument("-e", "--expression", action="append",
        dest="expressions", help="an expression to evaluate for each line")
    parser.add_argument('files', nargs='*',
        help="files to read as input. If used with --inplace, the files will be replaced with the output")
    parser.add_argument("--traceback", action="store_true", default=False,
        help="print a traceback on stderr when an expression fails for a line")

    args = parser.parse_args() if not argv else parser.parse_args(argv)

    pyle_evaluate(args.expressions, args.modules, args.inplace, args.files,
                  args.traceback)

if __name__ == '__main__':
    pyle()
