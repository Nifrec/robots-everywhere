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

Testcases for class Question in question.py
"""
import unittest
from robots_everywhere.question_gen.question import Question
from robots_everywhere.database.database_writer import Variable


class QuestionTestCase(unittest.TestCase):

    def test_repr_1(self):
        """
        Base case: str-typed Question
        """

        question = Question("TestQuestion",Variable(str, "TestVar"))
        expected = "Question('TestQuestion',Variable(str,'TestVar'))"
        result = repr(question)
        self.assertEqual(result, expected)

    def test_repr_2(self):
        """
        Base-case: str-typed Question
        """

        question = Question("TestQuestion1",Variable(str, "TestVar1"))
        expected = "Question(Variable(str,'TestVar1')):TestQuestion1"
        result = str(question)
        self.assertEqual(result, expected)

    def test__eq__1(self):
        """
        Both inputs should be equal.
        """
        que_1 = Question("TestQuestion1",Variable(str, "TestVar1"))
        que_2 = Question("TestQuestion1",Variable(str, "TestVar1"))
        self.assertEqual(que_1, que_2)

    def test__eq__2(self):
        """
        Content different.
        """
        que_1 = Question("TestQuestion1",Variable(str, "TestVar1"))
        que_2 = Question("TestQuestion2",Variable(str, "TestVar1"))
        self.assertNotEqual(que_1, que_2)

    def test__eq__3(self):
        """
        Variable different.
        """
        que_1 = Question("TestQuestion1",Variable(str, "TestVar1"))
        que_2 = Question("TestQuestion1",Variable(str, "TestVar2"))
        self.assertNotEqual(que_1, que_2)





if __name__ == '__main__':
    unittest.main()
