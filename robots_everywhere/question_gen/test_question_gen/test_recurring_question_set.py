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

Test cases for the class RecurringQuestionSet
"""

import unittest
from robots_everywhere.question_gen.recurring_question_set import WeekDay
from robots_everywhere.question_gen.recurring_question_set import RecurringQuestionSet
from robots_everywhere.question_gen.question import Question
from robots_everywhere.database.database import Variable
import time


class TestRecurringQuestionSet(unittest.TestCase):

    def setUp(self) -> None:
        """
        Scheduled time: Tuesday 7:30
        Start time: Monday 15:22, 22 March
        """
        start_time = 1616422958

        self.recurring_question = RecurringQuestionSet(
            {WeekDay(1)}, 7, 30,
            {Question("test", Variable(str, "my_var"))},
            start_time)

    def test_is_due_1(self):
        """
        Wednesday 15:22:38
        """
        timestamp = 1616595758
        test1 = self.recurring_question.is_due(timestamp)
        self.assertEqual(test1, True)

    def test_is_due_2(self):
        """
        Monday 23:22, 22 March
        """
        timestamp = 1616451758
        test2 = self.recurring_question.is_due(timestamp)
        self.assertEqual(test2, False)

    def test_is_due_3(self):
        """
        Monday 9:22
        """
        timestamp = 1616401358
        with self.assertRaises(RuntimeError):
            self.recurring_question.is_due(timestamp)


if __name__ == '__main__':
    unittest.main()
