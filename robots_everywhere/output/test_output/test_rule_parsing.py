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
    cut_rule_expression, extract_vars, substitute_vars, ParseResults, \
    substitute_quantifiers


class ParseExpressionTestCase(unittest.TestCase):

    def check_parse(self, expression: str, expected: ParseResults):
        result = parse_expression(expression)

        self.assertEqual(expected.trigger_expr, result.trigger_expr)
        self.assertEqual(expected.message_expr, result.message_expr)
        self.assertSetEqual(expected.vars_dict, result.vars_dict)

    def test_parse_1(self):
        expression = "RULE mean(sleep(last 3)) <= work(first 1) | work(first 1)"
        expected_trigger = "mean(vars_dict['sleep'][-3:]) <= vars_dict['work'][:1]"
        expected_message = "vars_dict['work'][:1]"
        expected_vars_dict = {"sleep", "work"}
        expected = ParseResults(expected_trigger, expected_message,
                                "0", expected_vars_dict)
        self.check_parse(expression, expected)

    def test_parse_2(self):
        expression = "RULE mean(sleep(last 3)) <= work(first 1) | work(first 1)"
        expected_trigger = "mean(vars_dict['sleep'][-3:]) <= vars_dict['work'][:1]"
        expected_message = "vars_dict['work'][:1]"
        expected_vars_dict = {"sleep", "work"}
        result = parse_expression(expression)

        self.assertEqual(expected_trigger, result.trigger_expr)
        self.assertEqual(expected_message, result.message_expr)
        self.assertSetEqual(expected_vars_dict, result.vars_dict)

    def test_parse_with_eval(self):
        expression = ("RULE mean(sleep(last 3)) <= work(first 1) "
                      "| work(first 1) | sleep(last 1)")
        expected_trigger = "mean(vars_dict['sleep'][-3:]) <= vars_dict['work'][:1]"
        expected_message = "vars_dict['work'][:1]"
        expected_eval = "vars_dict['work'][-1]"
        expected_vars_dict = {"sleep", "work"}
        expected = ParseResults(expected_trigger, expected_message,
                                expected_eval, expected_vars_dict)
        self.check_parse(expression, expected)


class SubstituteQuantifiersTestCase(unittest.TestCase):

    def test_substitute_allbutlast(self):
        expression = "hello world how(allbutlast 3) oh?"
        expected = "hello world how[:-3] oh?"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_substitute_allbutfirst(self):
        expression = "sleep(allbutfirst 3)- 10"
        expected = "sleep[3:]- 10"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_substitute_first(self):
        expression = "sleep(first 3)- 10"
        expected = "sleep[:3]- 10"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_substitute_last(self):
        expression = "sleep(last 3) -~- 10 :)"
        expected = "sleep[-3:] -~- 10 :)"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_substitute_extra_whitespaces(self):
        """
        Extra whitespaces within the brackets are allowed
        as long as they leave the keyword intact.
        """
        expression = "sleep(      allbutfirst    3   )"
        expected = "sleep[3:]"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_substitute_without_space(self):
        """
        A whitespace between the quentifier keyword and the index
        is not enforced.
        """
        expression = "sleep(first3)- 10"
        expected = "sleep[:3]- 10"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_preserve_mean(self):
        """
        The 'mean' keyword also uses brackets.
        They must be retained!
        """
        expression = "mean(something(allbutfirst2))"
        expected = "mean(something[2:])"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_substitute_multiple(self):
        """
        Multiple quantifiers should all be substituted.
        """
        expression = "sleep(last 3) + meh(allbutlast2) + fish(last1)"
        expected = "sleep[-3:] + meh[:-2] + fish[-1:]"
        result = substitute_quantifiers(expression)
        self.assertEqual(expected, result)

    def test_error_if_float(self):
        """
        Floating point indices are sementically undefined
        and are hence not allowed.
        """
        expression = "my_var(last 3.5)"
        with self.assertRaises(ValueError):
            substitute_quantifiers(expression)

    def test_error_if_missing_index(self):
        """
        The end/starting index may not be missing.
        Also not in the case of 'first' or 'last'.
        """
        expression = "my_var(last)"
        with self.assertRaises(ValueError):
            substitute_quantifiers(expression)

    def test_error_if_index_is_str(self):
        """
        Indices must be int.
        """
        expression = "my_var(last ten)"
        with self.assertRaises(ValueError):
            substitute_quantifiers(expression)

    def test_error_if_unrecognized_range_keyword(self):
        """
        The keyword must be 'first', 'allbutfirst', 'allbutlast' or 'last'.
        """
        expression = "my_var(some 3)"
        with self.assertRaises(ValueError):
            substitute_quantifiers(expression)


class Substitutevars_dictTestCase(unittest.TestCase):

    def test_substitute_1(self):
        vars_dict = {"hello", "world"}
        expression = "oh hello dear world!"
        expected = "oh vars_dict['hello'] dear vars_dict['world']!"
        result = substitute_vars(expression, vars_dict)
        self.assertEqual(result, expected)


class Extractvars_dictTestCase(unittest.TestCase):

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
        expected = ("my_var < mean(some_other_var(first 10)) + 10", "11", "0")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_2(self):
        """
        Corner case: no whitespace after "rule". Should not matter.
        """
        input_str = "ruLESS than|this --"
        expected = ("ss than", "this --", "0")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_3(self):
        """
        Corner case: a whitespace before "rule". Should not matter.
        """
        input_str = " RuLe than   |this --  "
        expected = ("than", "this --", "0")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_4(self):
        """
        Base case: output is always lower case.
        """
        input_str = "rule HelloWorld   | ."
        expected = ("helloworld", ".", "0")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_with_third_expression_1(self):
        """
        Base case: third expression should be surrounded by "tanh(" and ")".
        """
        input_str = "rule 1 | 2 | 3"
        expected = ("1", "2", "tanh(3)")
        result = cut_rule_expression(input_str)
        self.assertTupleEqual(expected, result)

    def test_cut_with_third_expression_1(self):
        """
        Base case: third expression should be surrounded by "tanh(" and ")",
        even if it contains non-trailing & non-leading whitespaces.
        """
        input_str = "rule 1 | 2 | mean(2*a + 3) - 4"
        expected = ("1", "2", "tanh(mean(2*a + 3) - 4)")
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

    def test_cut_right_empty_three_expression(self):
        """
        Corner case: error needed if the third column contains no expression,
        but two "|"s are given.
        """
        input_str = "rule 1+a  | 3 | "
        with self.assertRaises(ValueError):
            cut_rule_expression(input_str)


if __name__ == "__main__":
    unittest.main()
