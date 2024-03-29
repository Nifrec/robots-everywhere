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

Testcases for the class Rule from rule.py
"""
import unittest
import pandas as pd
from robots_everywhere.output.rules import EvaluationExpression, \
    MessageExpression, TriggerExpression, Rule

from robots_everywhere.database.database import DatabaseReader

class MockDatabaseReader(DatabaseReader):
    
    def __init__(self, output: pd.DataFrame):
        self.output = output

    def get_rows_of_vars(self, _) -> pd.DataFrame:
        return self.output

class RuleFireableTestCase(unittest.TestCase):

    def setUp(self):
        expression = "vars_dict['my_var'][-1:] > vars_dict['my_var'][:1]"
        trigger = TriggerExpression(expression, set(['my_var']))
        messager = MessageExpression("'m'", set([]))
        evaluator = EvaluationExpression("0", set([]))
        self.rule = Rule(trigger, messager, evaluator)

    def test_fireable_true(self):
        """
        Base case: the trigger expression simply does hold,
        and is evaluated only once.
        """
        values = {'my_var':[0.1, 1.1]}
        db_reader = MockDatabaseReader(values)

        self.assertTrue(self.rule.check_fireable(db_reader))

    def test_fireable_false(self):
        """
        Base case: the trigger expression simply doesn't hold.
        """
        values = {'my_var':[2.0, 1.1]}
        db_reader = MockDatabaseReader(values)

        self.assertFalse(self.rule.check_fireable(db_reader))

    def test_fireable_after_firing(self):
        """
        A Rule may not be fireable, if it has been fired and the
        relevant variables in the database have no new values.
        Even if the trigger expression evaluates to True.
        """
        values = {'my_var':[1.0, 1.5]}
        db_reader = MockDatabaseReader(values)
        self.rule.fire(db_reader)
        self.assertFalse(self.rule.check_fireable(db_reader))

    def test_fireable_after_firing_and_new_data_true(self):
        """
        A Rule may should become fireable if changes where
        made in variables related to its trigger, 
        and if the trigger expression evaluates to True.

        Case in which the new data still passes the trigger.
        """
        values = {'my_var':[1.0, 1.5]}
        db_reader = MockDatabaseReader(values)
        self.rule.fire(db_reader)
        db_reader.output = {'my_var':[1.0, 1.5, 3.0]}
        self.assertTrue(self.rule.check_fireable(db_reader))

    def test_fireable_after_firing_and_new_data_false(self):
        """
        A Rule may should become fireable if changes where
        made in variables related to its trigger, 
        and if the trigger expression evaluates to True.

        Case in which the new data does not pass the trigger.
        """
        values = {'my_var':[1.0, 1.5]}
        db_reader = MockDatabaseReader(values)
        self.rule.fire(db_reader)
        db_reader.output = {'my_var':[1.0, 1.5, 1.0]}
        self.assertFalse(self.rule.check_fireable(db_reader))

    def test_fire_error_if_not_fireable(self):
        """
        A RuntimeError should be raised when calling Rule.fire()
        if it is not fireable.
        """
        values = {'my_var':[2.0, 1.1]}
        db_reader = MockDatabaseReader(values)

        with self.assertRaises(RuntimeError):
            self.rule.fire(db_reader)

    def test_fire_output(self):
        values = {'my_var':[1.0, 1.5]}
        db_reader = MockDatabaseReader(values)
        message, eval = self.rule.fire(db_reader)
        self.assertEqual(eval, 0)
        self.assertEqual(message, 'm')

if __name__ == "__main__":
    unittest.main()