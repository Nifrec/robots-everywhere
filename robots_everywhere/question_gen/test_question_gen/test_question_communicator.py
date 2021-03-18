"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021  Lulof Pirée

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

Testcases for class QuestionCommunicator.
"""
from typing import Set
import unittest
import multiprocessing

from robots_everywhere.database.database import Variable
from robots_everywhere.message import AnswerMessage
from robots_everywhere.question_gen.question_communicator \
    import QuestionCommunicator
from robots_everywhere.question_gen.question_occurrence \
    import QuestionOccurrence
from robots_everywhere.question_gen.question_schedule import QuestionSchedule
from robots_everywhere.database.test_database.test_database import \
    remove_database, TEST_DB_NAME, DatabaseWriter


class MockQuestionSchedule(QuestionSchedule):
    """
    Mock implementation that always returns the same output
    to get_new_occurences().
    """

    def __init__(self, output: Set[QuestionOccurrence]):
        self.output = output

    def get_new_occurences(self, _) -> Set[QuestionOccurrence]:
        return self.output


class QuestionCommunicatorTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.db = DatabaseWriter(TEST_DB_NAME)

        self.var_foo = Variable(int, "foo")
        self.db.create_new_var(self.var_foo)

    def test_handling_answer_in_pipe(self):
        """
        Run the mainloop of QuestionCommunicator
        for one timestep, while there is an Answer in the pipe.
        This should be stored as in the database,
        and an InsertCommand should be stored with the same ID.
        """
        communicator_end, testsuite_end = multiprocessing.Pipe(True)


        answer = AnswerMessage(id=12345, var=self.var_foo, value=13)

        
        testsuite_end.send(answer)

        communicator = QuestionCommunicator(communicator_end, self.db,
                                            MockQuestionSchedule())

        communicator.mainloop(0.001, 1)

        result = self.db.get_rows_of_vars([self.var_foo])
        expected = {"foo": [13]}

        self.assertDictEqual(result, expected)

        self.fail("TODO: also test InsertCommand!")


if __name__ == "__main__":
    unittest.main()
