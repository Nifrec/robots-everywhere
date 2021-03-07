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

Testcases for the source file rules.py.
"""
import unittest
from robots_everywhere.output.rules import parse_expression, \
    cut_rule_expression, extract_vars

class ExtractVarsTestCase(unittest.TestCase):

    def test_extract_vars(self):
        expression = "my_var, my_other_var, (some_var)"
        expected = {"my_var", "my_other_var", "some_var"}
        self.assertSetEqual(extract_vars(expression), expected)

    def test_ignore_mean(self):
        """
        The substring "mean" should always be ignored.
        """
        expression = "my_varmean(my_other_var)some_varmeana)"
        expected = {"my_var", "my_other_var", "some_var", "a"}
        self.assertSetEqual(extract_vars(expression), expected)

    def test_ignore_first(self):
        """
        The substring "first" should always be ignored.
        """
        expression = "my_varfirst(my_other_var)some_varfirsta)"
        expected = {"my_var", "my_other_var", "some_var", "a"}
        self.assertSetEqual(extract_vars(expression), expected)

    def test_ignore_last(self):
        """
        The substring "last" should always be ignored.
        """
        expression = "my_varlast(my_other_var)some_varlasta)"
        expected = {"my_var", "my_other_var", "some_var", "a"}
        self.assertSetEqual(extract_vars(expression), expected)

    def test_ignore_allbut(self):
        """
        The substring "allbut" should always be ignored.
        """
        expression = "my_varallbut(my_other_var)some_varallbuta)"
        expected = {"my_var", "my_other_var", "some_var", "a"}
        self.assertSetEqual(extract_vars(expression), expected)

    def test_ignore_combo(self):
        """
        Any concatenation of the ignored substrings should also be ignored.
        """
        expression = "helloallbutfirstworld)"
        expected = {"hello", "world"}
        self.assertSetEqual(extract_vars(expression), expected)

class CutRuleExpressionTestCase(unittest.TestCase):
    
    def test_error_if_not_starts_correct(self):
        """
        Each rule should be prefixed with "rule".
        Case insensitive.
        """
        bad_rule = "hello world"
        with self.assertRaises(ValueError):
            cut_rule_expression(bad_rule)

    def test_error_if_missing_bar(self):
        """
        Each rule should contain a "|".
        """
        bad_rule = "rule a > 2"
        with self.assertRaises(ValueError):
            cut_rule_expression(bad_rule)

    def test_cut_1(self):
        """
        Base case: whitespaces around expression should be trimmer,
        and should be case insensitive to "rule".
        """
        input_str = "RULE my_var < mean(some_other_var(first 10)) + 10 | 11 "
        expected = ("my_var < mean(some_other_var(first 10)) + 10", "11")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_2(self):
        """
        Corner case: no whitespace after "rule". Should not matter.
        """
        input_str = "ruLESS than|this --"
        expected = ("ss than", "this --")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_3(self):
        """
        Corner case: a whitespace before "rule". Should not matter.
        """
        input_str = " RuLe than   |this --  "
        expected = ("than", "this --")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_4(self):
        """
        Base case: output is always lower case.
        """
        input_str = "rule HelloWorld   | ."
        expected = ("helloworld", ".")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_left_empty(self):
        """
        Corner case: error needed if left side contains no expression.
        """
        input_str = "rule   | 1+a"
        with self.assertRaises(ValueError):
            cut_rule_expression(input_str)

    def test_cut_right_empty(self):
        """
        Corner case: error needed if right side contains no expression.
        """
        input_str = "rule 1+a  |  "
        with self.assertRaises(ValueError):
            cut_rule_expression(input_str)

if __name__ == "__main__":
    unittest.main()