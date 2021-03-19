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
from robots_everywhere.question_gen.question import Question
from typing import Set
import unittest
import multiprocessing
import time

from robots_everywhere.database.database import Variable
from robots_everywhere.message import AnswerMessage, QuestionMessage
from robots_everywhere.question_gen.question_communicator \
    import QuestionCommunicator
from robots_everywhere.question_gen.question_occurrence \
    import QuestionOccurrence
from robots_everywhere.question_gen.question_schedule import QuestionSchedule
from robots_everywhere.database.test_database.test_database import \
    remove_database, TEST_DB_NAME, DatabaseWriter
from robots_everywhere.database.command import InsertCommand

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
                                            MockQuestionSchedule(set()))

        communicator.mainloop(0, 1)

        result = self.db.get_rows_of_vars([self.var_foo])
        expected = {"foo": [13]}

        self.assertDictEqual(result, expected)

        result_commands = communicator._QuestionCommunicator__executed_commands
        self.assertEqual(len(result_commands), 1)
        self.assertIsInstance(result_commands[0], InsertCommand)
        self.assertTrue(result_commands[0].is_executed)
        self.assertIs(result_commands[0].variable, self.var_foo)
        self.assertAlmostEqual(result_commands[0].timestamp, time.time())

    def test_handling_2_answers_in_pipe(self):
        """
        One timestep, 2 answers in pipe. Both values should be stored
        in the database, in correct order.
        """
        communicator_end, testsuite_end = multiprocessing.Pipe(True)
        answer_1 = AnswerMessage(id=1, var=self.var_foo, value=1)
        answer_2 = AnswerMessage(id=2, var=self.var_foo, value=2)
        testsuite_end.send(answer_1)
        testsuite_end.send(answer_2)

        communicator = QuestionCommunicator(communicator_end, self.db,
                                            MockQuestionSchedule(set()))

        communicator.mainloop(0, 1)

        result = self.db.get_rows_of_vars([self.var_foo])
        expected = {"foo": [1, 2]}

        self.assertDictEqual(result, expected)

        result_commands = communicator._QuestionCommunicator__executed_commands
        self.assertEqual(len(result_commands), 2)

    def test_handling_answers_2_timesteps(self):
        """
        Two timesteps, 1 answer in pipe each timestep. 
        Both values should be stored
        in the database, in correct order.

        Unfortunately need to interrupt the mainloop and restart,
        otherwise it is too difficult to send an answer
        in-between the timesteps.
        """
        communicator_end, testsuite_end = multiprocessing.Pipe(True)
        answer_1 = AnswerMessage(id=1, var=self.var_foo, value=1)
        answer_2 = AnswerMessage(id=2, var=self.var_foo, value=2)
        

        communicator = QuestionCommunicator(communicator_end, self.db,
                                            MockQuestionSchedule(set()))

        testsuite_end.send(answer_1)
        communicator.mainloop(0, 1)
        testsuite_end.send(answer_2)
        communicator.mainloop(0, 1)

        result = self.db.get_rows_of_vars([self.var_foo])
        expected = {"foo": [1, 2]}

        self.assertDictEqual(result, expected)

        result_commands = communicator._QuestionCommunicator__executed_commands
        self.assertEqual(len(result_commands), 2)

    def test_putting_question_in_pipe(self):
        """
        Run the mainloop of QuestionCommunicator
        for one timestep. 
        The given QuestionSchedule generates one set of QuestionOccurrences,
        with one question. 
        The QuestionCommunicator should put a corresponding
        QuestionMessage in the Queue.
        """
        communicator_end, testsuite_end = multiprocessing.Pipe(True)

        question = Question("How are you?", self.var_foo)
        schedule = MockQuestionSchedule({QuestionOccurrence(question, 123)})

        communicator = QuestionCommunicator(communicator_end, self.db, schedule)
        communicator.mainloop(0, 1)

        self.assertTrue(testsuite_end.poll())
        result = testsuite_end.recv()
        self.assertIsInstance(result, QuestionMessage)
        self.assertEqual(result.id, 123)
        self.assertEqual(result.text, "How are you?")
        self.assertEqual(result.variable, self.var_foo)
        self.assertFalse(testsuite_end.poll())

    def test_putting_questions_in_pipe_mult_questions(self):
        """
        Run one timestep, multiple questions given,
        multiple questions in pipe expected.
        """
        communicator_end, testsuite_end = multiprocessing.Pipe(True)

        question_1 = Question("How are you?", self.var_foo)
        question_2 = Question("Walk to Hell!", self.var_foo)
        schedule = MockQuestionSchedule(
            {QuestionOccurrence(question_1, 123),
             QuestionOccurrence(question_2, 666)})

        communicator = QuestionCommunicator(communicator_end, self.db, schedule)
        communicator.mainloop(0, 1)

        self.assertTrue(testsuite_end.poll())
        testsuite_end.recv() # First output already tested in test above.
        self.assertFalse(testsuite_end.poll())
        result = testsuite_end.recv()
        self.assertIsInstance(result, QuestionMessage)
        self.assertEqual(result.id, 666)
        self.assertEqual(result.text, "Walk to Hell!")
        self.assertEqual(result.variable, self.var_foo)
        self.assertFalse(testsuite_end.poll())

    def test_putting_questions_in_pipe_mult_questions(self):
        """
        One question occurs per timestep.
        So after 2 timesteps, there should be 2 questions in the pipe.
        """
        communicator_end, testsuite_end = multiprocessing.Pipe(True)

        question_1 = Question("How are you?", self.var_foo)
        schedule = MockQuestionSchedule(
            {QuestionOccurrence(question_1, 123)})

        communicator = QuestionCommunicator(communicator_end, self.db, schedule)
        communicator.mainloop(0, 2)

        self.assertTrue(testsuite_end.poll())
        testsuite_end.recv() # Question from first timestep
        self.assertTrue(testsuite_end.poll())
        testsuite_end.recv() # Question from second timestep
        self.assertFalse(testsuite_end.poll())

if __name__ == "__main__":
    unittest.main()
