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
    def std_run(self, code, input_string, modules=None):
        cmd = ['python', 'pyle.py', '-e', code]
        if modules:
            cmd += ['-m'] + [modules]
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        return p.communicate(input=input_string)[0]

    def testFirst5(self):
        output = self.std_run('line[:5]', test_input_a)

        self.assertEquals(output, """A few
dance
short
""")

    def testFirst5FromFile(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            tmp_file.write(test_input_a)
            tmp_file.close()

            p = Popen(['python', 'pyle.py', '-e', 'line[:5]', tmp_file.name], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = p.communicate()[0]

            self.assertEquals(output, """A few
dance
short
""")
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
short
""")

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
