#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT
import tempfile
import unittest
import os
import sys
import operator

test_input_a = """A few characters
dance on the
short little lines"""

test_input_b = """
This line protected by cowboys.
An alien? This box is FILLED with aliens!"
"""


class TestPyle(unittest.TestCase):
    def std_run(self, code, input_string, more_code=None, modules=None,
                print_traceback=False):
        cmd = [sys.executable, 'pyle.py', '-e', code]
        if more_code:
            cmd.extend(reduce(operator.add, [['-e', c] for c in more_code]))
        if modules:
            cmd += ['-m'] + [modules]
        if print_traceback:
            cmd += ['--traceback']
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        return p.communicate(input=input_string)[0]

    def test_first_five_lines(self):
        output = self.std_run('line[:5]', test_input_a)

        self.assertEquals(output, """A few
dance
short""")

    def tes_first_five_line_from_file(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp_file.write(test_input_a)
            tmp_file.close()

            p = Popen([sys.executable, 'pyle.py', '-e', 'line[:5]', tmp_file.name], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
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

            p = Popen([sys.executable, 'pyle.py', '-ie', code, tmp_file.name], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = p.communicate()[0]

            self.assertEquals(output, '')

            with open(tmp_file.name, 'rb') as tmp_file_2:
                output = tmp_file_2.read()

        finally:
            os.unlink(tmp_file.name)
        return output

    def test_first_five_in_place(self):
        output = self.in_place_run('line[:5]', test_input_a)
        self.assertEquals(output, """A few
dance
short""")

    def test_aliens_substitution(self):
        output = self.in_place_run(r"re.sub(r'alien(s|)?', r'angel\1', line)", test_input_b)
        self.assertEquals(output, """
This line protected by cowboys.
An angel? This box is FILLED with angels!"
""")

    def test_unicode_input(self):
        test_str = 'Segla f\xf6rutan vind\n'
        output = self.std_run('line', test_str)
        self.assertEquals(output, test_str)

    def test_unicode_output(self):
        output = self.std_run('u"test"', "\n")
        self.assertEquals(output, "test\n")

    def test_binary_input(self):
        test_str = '\x00\x01\x02'
        output = self.std_run('line', test_str)
        self.assertEquals(output, test_str)

    def test_error_message(self):
        output = self.std_run('int(line)', "1\nPylo\n3\n")
        self.assertEquals(output, "1\nAt <stdin>:1 ('Pylo'): `int(line)`: invalid literal for int() with base 10: 'Pylo'\n3\n")

    def test_traceback(self):
        output = self.std_run('int(line)', "1\nPylo\n3\n", print_traceback=True)
        self.assertTrue("invalid literal for int() with base 10" in output)
        self.assertTrue("Traceback (most recent call last)" in output)

    def test_multiple_expressions(self):
        output = self.std_run('re.sub("a", "B", line)', 'aaa',
                              more_code=['re.sub("B", "c", line)', 'line[:2]'])
        self.assertEquals(output, 'cc')
