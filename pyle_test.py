#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT
import tempfile
import unittest
import os

test_input_a = """A few characters
dance on the
short little lines"""

test_input_b = """
This line protected by cowboys.
An alien? This box is FILLED with aliens!"
"""


class TestPyle(unittest.TestCase):
    def std_run(self, code, input_string, modules=None, print_traceback=False):
        cmd = ['python', 'pyle.py', '-e', code]
        if modules:
            cmd += ['-m'] + [modules]
        if print_traceback:
            cmd += ['--traceback']
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        return p.communicate(input=input_string)[0]

    def testFirst5(self):
        output = self.std_run('line[:5]', test_input_a)

        self.assertEquals(output, """A few
dance
short""")

    def testFirst5FromFile(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp_file.write(test_input_a)
            tmp_file.close()

            p = Popen(['python', 'pyle.py', '-e', 'line[:5]', tmp_file.name], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = p.communicate()[0]

            self.assertEquals(output, """A few
dance
short""")
        finally:
            os.unlink(tmp_file.name)

    def in_place_run(self, code, input_string):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp_file.write(input_string)
            tmp_file.close()

            p = Popen(['python', 'pyle.py', '-ie', code, tmp_file.name], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = p.communicate()[0]

            self.assertEquals(output, '')

            with open(tmp_file.name, 'rb') as tmp_file_2:
                output = tmp_file_2.read()

        finally:
            os.unlink(tmp_file.name)
        return output

    def testFirst5InPlace(self):
        output = self.in_place_run('line[:5]', test_input_a)
        self.assertEquals(output, """A few
dance
short""")

    def testAliens(self):
        output = self.in_place_run(r"re.sub(r'alien(s|)?', r'angel\1', line)", test_input_b)
        self.assertEquals(output, """
This line protected by cowboys.
An angel? This box is FILLED with angels!"
""")

    def testUtf(self):
        test_str = 'Segla f\xf6rutan vind\n'
        output = self.std_run('line', test_str)
        self.assertEquals(output, test_str)

    def testBinary(self):
        test_str = '\x00\x01\x02'
        output = self.std_run('line', test_str)
        self.assertEquals(output, test_str)

    def testErrorMessage(self):
        output = self.std_run('int(line)', "1\nPylo\n3\n")
        self.assertEquals(output, "1\nAt <stdin>:1 ('Pylo'): invalid literal for int() with base 10: 'Pylo'\n3\n")

    def testTraceback(self):
        output = self.std_run('int(line)', "1\nPylo\n3\n", print_traceback=True)
        # FIXME This test shouldn't depend on source code line numbers to succeed.
        self.assertEquals(output, """1
At <stdin>:1 ('Pylo'): invalid literal for int() with base 10: 'Pylo'
Traceback (most recent call last):
  File "pyle.py", line 69, in pyle_evaluate
    out_line = eval(command, eval_globals, eval_locals)
  File "<string>", line 1, in <module>
ValueError: invalid literal for int() with base 10: 'Pylo'
3
""")


