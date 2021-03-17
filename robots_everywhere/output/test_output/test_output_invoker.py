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
import time
import unittest
import numpy as np
from typing import Any, Dict


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

        trig = TriggerExpression(
            "mean(vars_dict['foo'][-2:]) > mean(vars_dict['bar'][-3:])",
            {"foo", "bar"})
        mess = MessageExpression("vars_dict['foo'][-1:]", {"foo"})
        eval = EvaluationExpression("vars_dict['bar'][-1:] - vars_dict['foo'][-1:]",
                                    {"foo", "bar"})
        self.rule = Rule(trig, mess, eval)

    def test_find_fireable_rules(self):
        invoker = OutputInvoker([self.rule], None, self.db)
        result = invoker._find_fireable_rules()

        self.assertTrue(self.rule.check_fireable(self.db), msg="Testcase broken")
        self.assertSequenceEqual(result, [self.rule])


if __name__ == "__main__":
    unittest.main()