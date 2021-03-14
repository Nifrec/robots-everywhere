"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021  Edwin Steenkamer

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Testcases for class QuestionOccurrence in question_occurrence.py
"""
import unittest
from robots_everywhere.question_gen.question import Question
from robots_everywhere.question_gen.question_occurrence import QuestionOccurrence
from robots_everywhere.database.database_writer import Variable


class MyTestCase(unittest.TestCase):
    def test_repr(self):
        occurrence = QuestionOccurrence(Question("TestQuestion",Variable(str, "TestVar")), 0)
        expected = "0: 'TestQuestion'"
        result = str(occurrence)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
