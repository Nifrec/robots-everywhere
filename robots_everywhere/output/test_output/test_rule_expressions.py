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

Testcases for the classes RuleExpression, TriggerExpression, MessageExpression
and EvaluationExpression from the file rules.py.
"""
import unittest
import numpy as np
from typing import Any, Dict
from robots_everywhere.database.database_writer import Variable
from robots_everywhere.output.rules import RuleExpression, \
    TriggerExpression, MessageExpression, EvaluationExpression


class TestingRuleExpression(RuleExpression):
    """
    Same as RuleExpression, but instantiable as the abstract method
    is overridden with an empty implementation.
    """

    def _hook_check_output_value(self, _) -> bool:
        return True


class RuleExpressionTestCase(unittest.TestCase):

    def check_rule_expression(self,
                              expression: str,
                              vars: Dict[str, np.ndarray],
                              expected: Any):
        rule_expr = TestingRuleExpression(expression, set(vars.keys()))
        result = rule_expr(vars)
        self.assertAlmostEqual(result, expected)

    def test_get_variables(self):
        expression = "0"
        vars = {
            "var_1",
            "var_2"
        }
        rule_expr = TestingRuleExpression(expression, vars)
        self.assertSetEqual(rule_expr.variable_names, vars)

    def test_call_bool_false(self):
        """
        Basic case: two variables, boolean rule evaluating to False.
        """
        expression = "vars['var_1'][0] > vars['var_2'][0]"
        vars = {
            'var_1': np.array([10]),
            'var_2': np.array([11])
        }
        expected = False
        self.check_rule_expression(expression, vars, expected)

    def test_call_bool_true(self):
        """
        Basic case: one variables, boolean rule evaluating to True.
        """
        expression = "vars['var_1'][3] > 3"
        vars = {
            'var_1': np.array([2, 1, 1, 3.1, -.01, 2.3]),
        }
        expected = True
        self.check_rule_expression(expression, vars, expected)

    def test_call_number_with_square(self):
        """
        Basic case: two variables, numeric output.
        """
        expression = "vars['var_1'][0] + vars['var_2'][2]**2"
        vars = {
            'var_1': np.array([10, 12, 13]),
            'var_2': np.array([9, 8, 7])
        }
        expected = 10 + 7**2
        self.check_rule_expression(expression, vars, expected)

    def test_call_number_with_modulo(self):
        """
        Basic case: one variable, with modulo.
        """
        expression = "vars['meh'][2] % vars['meh'][0]"
        vars = {
            'var_1': np.array([10, 12, 13]),
            'meh': np.array([9, 8, 100])
        }
        expected = 100 % 9
        self.check_rule_expression(expression, vars, expected)

    def test_call_number_with_mean(self):
        """
        Basic case: one variable, with mean.
        """
        expression = "mean(vars['var_1'][:3])"
        vars = {
            'var_1': np.array([10, 12, 13, 14, 15, 16]),
        }
        expected = (10 + 12 + 13) / 3
        self.check_rule_expression(expression, vars, expected)

    def test_call_array(self):
        """
        Basic case: outputting an array is allowed.
        """
        expression = "vars['var_1'][:3] + vars['var_1'][3:]"
        vars = {
            'var_1': np.array([10, 12, 13, 14, 15, 16]),
        }
        expected = np.array([24, 27, 29])
        rule_expr = TestingRuleExpression(expression, set(vars.keys()))
        result = rule_expr(vars)
        np.testing.assert_allclose(result, expected)


class RuleExpressionSubclassesTestCase(unittest.TestCase):
    """
    Test if the hook methods of the subclasses of RuleExpression
    behave as expected.
    """

    def test_trigger_expression_hook(self):
        """
        The output must be a single Boolean value.
        """
        trigger = TriggerExpression("0", set([]))
        self.assertTrue(trigger._hook_check_output_value(True))
        self.assertTrue(trigger._hook_check_output_value(False))
        self.assertTrue(trigger._hook_check_output_value(np.array([True])))
        self.assertTrue(trigger._hook_check_output_value(np.array([False])))
        self.assertFalse(trigger._hook_check_output_value(1))
        self.assertFalse(trigger._hook_check_output_value(1.0))
        self.assertFalse(trigger._hook_check_output_value(np.array([1.0])))
        self.assertFalse(trigger._hook_check_output_value(
            np.array([True, True])))


if __name__ == "__main__":
    unittest.main()
