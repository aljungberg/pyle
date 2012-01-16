#!/usr/bin/env python

"""

Pyle allows you to use Python as a replacement for command line tools such
as `sed` or `perl`. It reads its standard input and evaluates each line with
the expression specified, outputting the results on standard out.
Optionally, it can operate on a list of filenames instead in which case each
file is read and processed in order. The variables `line`, representing the
current input line being processed, `words`, representing the current
line split by whitespace, `num`, the 0 index line number in the current
file, and `filename`, the name of the current file, are available to the
expression. In addition the `re` module is available. To supress printing
of a line, return None.

"""

import argparse
import cStringIO as StringIO
import re
import sys
import traceback

STANDARD_MODULES = ['re']


def pyle_evaluate(command=None, modules=None, inplace=False, files=None):
    eval_globals = {}

    modules = STANDARD_MODULES + (modules or [])
    for module_arg in modules:
        for module in module_arg.strip().split(","):
            module = module.strip()
            if module:
                eval_globals[module] = __import__(module)

    if not command:
        # Default 'do nothing' program
        command = 'line'

    files = files or ['-']
    for file in files:
        if file == '-':
            file = sys.stdin

        out_buf = sys.stdout if not inplace else StringIO.StringIO()

        with (open(file, 'rb') if not hasattr(file, 'read') else file) as in_file:
            for num, line in enumerate(in_file.readlines()):
                line = line[:-1]
                words = [word.strip() for word in re.split(r'\s+', line) if word]
                eval_locals = {'line': line, 'words': words, 'filename': in_file.name, 'num': num}
                try:
                    out_line = eval(command, eval_globals, eval_locals)
                except Exception:
                    traceback.print_exc(None, sys.stderr)
                else:
                    if out_line is None:
                        continue

                    # If the result is something list-like or iterable, output each item space separated.
                    if not isinstance(out_line, str):
                        try:
                            out_line = u' '.join(unicode(part) for part in out_line)
                        except:
                            # Guess it wasn't a list after all.
                            out_line = unicode(out_line)

                    out_line = out_line or u''
                    out_buf.write(out_line + u'\n')
        if inplace:
            with open(file, 'wb') as out_file:
                out_file.write(out_buf.getvalue())
            out_buf.close()


def pyle(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("-m", "--modules", dest="modules", action='append',
        help="import MODULE before evaluation. May be specified more than once.")
    parser.add_argument("-i", "--inplace", dest="inplace", action='store_true', default=False,
        help="edit files in place. When used with file name arguments, the files will be replaced by the output of the evaluation")
    parser.add_argument("-e", "--expression", dest="expression",
        help="the statement to evaluate on each line")
    parser.add_argument('files', nargs='*',
        help="files to read as input. If used with --inplace, the files will be replaced with the output")

    args = parser.parse_args() if not argv else parser.parse_args(argv)

    pyle_evaluate(args.expression, args.modules, args.inplace, args.files)

if __name__ == '__main__':
    pyle()
