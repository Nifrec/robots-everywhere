"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021 Lulof Pirée

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

Testcases for the class OutputInvoker.
"""
from robots_everywhere.message import OutputMessage
import time
import unittest
import numpy as np
from typing import Any, Dict
import multiprocessing

from robots_everywhere.database.database import Variable

from robots_everywhere.database.test_database.test_database import \
    remove_database, TEST_DB_NAME, DatabaseWriter
from robots_everywhere.output.rules import Rule, RuleExpression, \
    TriggerExpression, MessageExpression, EvaluationExpression
from robots_everywhere.output.output_invoker import OutputInvoker


class OuputInvokerTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.db = DatabaseWriter(TEST_DB_NAME)

        self.var_1 = Variable(int, "foo")
        self.db.create_new_var(self.var_1)
        self.db.insert_new_value_of_var(self.var_1, 10, 1)
        self.db.insert_new_value_of_var(self.var_1, 11, 2)
        self.db.insert_new_value_of_var(self.var_1, 12, 3)
        self.db.insert_new_value_of_var(self.var_1, 13, 4)
        self.db.insert_new_value_of_var(self.var_1, 14, 5)

        self.var_2 = Variable(float, "bar")
        self.db.create_new_var(self.var_2)
        self.db.insert_new_value_of_var(self.var_2, 10.1, 1)
        self.db.insert_new_value_of_var(self.var_2, 11.1, 2)
        self.db.insert_new_value_of_var(self.var_2, 12.1, 3)
        self.db.insert_new_value_of_var(self.var_2, 13.1, 4)
        self.db.insert_new_value_of_var(self.var_2, 14.1, 5)

        # Rule #1 is fireable.
        trig_1 = TriggerExpression(
            "mean(vars_dict['foo'][-2:]) > mean(vars_dict['bar'][-3:])",
            {"foo", "bar"})
        mess_1 = MessageExpression("vars_dict['bar'][-1:]", {"foo"})
        eval_1 = EvaluationExpression(
            "tanh(vars_dict['bar'][-1:] - vars_dict['foo'][-1:])",
            {"foo", "bar"})
        self.rule_1 = Rule(trig_1, mess_1, eval_1)

        # Rule #2 is not fireable.
        trig_2 = TriggerExpression(
            "vars_dict['foo'][:1] > mean(vars_dict['bar'][:2])", {"foo", "bar"})
        mess_2 = MessageExpression("vars_dict['foo'][-1:]", {"bar"})
        eval_2 = EvaluationExpression(
            "tanh(vars_dict['bar'][:1] - vars_dict['foo'][-1:])",
            {"foo", "bar"})
        self.rule_2 = Rule(trig_2, mess_2, eval_2)

    def test_find_fireable_rules(self):
        invoker = OutputInvoker([self.rule_1, self.rule_2], None, self.db)
        result = invoker._find_fireable_rules()

        self.assertTrue(self.rule_1.check_fireable(self.db),
                        msg="Testcase broken")

        self.assertFalse(self.rule_2.check_fireable(self.db),
                         msg="Testcase broken")

        self.assertSequenceEqual(result, [self.rule_1])

    def test_mainloop_sends_output(self):
        """
        Run the OutputInvoker one step. One rule should fire,
        test if a message received over the Pipe.
        """
        invoker_end, testcase_end = multiprocessing.Pipe(True)
        invoker = OutputInvoker([self.rule_1, self.rule_2],
                                invoker_end, self.db)

        invoker.mainloop(0.001, 1)

        self.assertTrue(testcase_end.poll(), "No message in the pipe")
        result: OutputMessage = testcase_end.recv()
        self.assertIsInstance(result, OutputMessage)
        self.assertAlmostEqual(result.evaluation, np.tanh(0.1))
        self.assertEqual(result.text, "[14.1]")
        self.assertFalse(self.rule_1.check_fireable(self.db))


if __name__ == "__main__":
    unittest.main()
