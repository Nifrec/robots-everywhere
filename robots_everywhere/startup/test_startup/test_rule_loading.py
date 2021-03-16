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

Testcases for class QuestionOccurrence in question_occurrence.py
"""
from robots_everywhere.output.rules import Rule
from robots_everywhere.database.database import DatabaseWriter, Variable
import unittest
from robots_everywhere.startup.rule_loading import \
    extract_lines_with_prefix_from_file, read_rules_from_file, read_vars_form_file
from robots_everywhere.database.test_database.test_database import remove_database, TEST_DB_NAME


class ExtractLinesWithPrefix(unittest.TestCase):

    def setUp(self) -> None:
        with open("test_file.txt",  'w') as fp:
            fp.writelines((
                "RULE some rule\n",
                "not a RULE\n",
                "Rule :)\n",
                "Chicken soup potatoes\n",
                "rule\n"
            ))

    def test_extract_lines(self):
        expected = ("RULE some rule\n", "Rule :)\n", "rule\n")
        result = extract_lines_with_prefix_from_file("test_file.txt", "RuLe")
        self.assertSequenceEqual(expected, result)


class ReadRulesFromFileTestCase(unittest.TestCase):

    def setUp(self):
        with open("test_file.txt",  'w') as fp:
            fp.writelines((
                "RULE sleep(last 2) > eat(first 2) | mean(sleep(last 10)) "
                "| sleep(last 1)\n",
                "RULE walk(last 1) | run(first 1) | skate(first 3)\n"
                "NOT A RULE\n",
                "VAR sleep int\n"
                "VAR skate float"
            ))

    def test_read_rules_from_file(self):
        rules = read_rules_from_file("test_file.txt")

        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)
        self.assertIsInstance(rules[0], Rule)
        self.assertIsInstance(rules[1], Rule)

        expected_trig = "vars_dict['sleep'][-2:] > vars_dict['eat'][:2]"
        expected_mess = "mean(vars_dict['sleep'][-10:])"
        expected_eval = "tanh(vars_dict['sleep'][-1:])"
        self.assertEqual(rules[0]._Rule__trigger._RuleExpression__expression,
                         expected_trig)
        self.assertEqual(rules[0]._Rule__messager._RuleExpression__expression,
                         expected_mess)
        self.assertEqual(rules[0]._Rule__evaluator._RuleExpression__expression,
                         expected_eval)

        expected_trig = "vars_dict['walk'][-1:]"
        expected_mess = "vars_dict['run'][:1]"
        expected_eval = "tanh(vars_dict['skate'][:3])"
        self.assertEqual(rules[1]._Rule__trigger._RuleExpression__expression,
                         expected_trig)
        self.assertEqual(rules[1]._Rule__messager._RuleExpression__expression,
                         expected_mess)
        self.assertEqual(rules[1]._Rule__evaluator._RuleExpression__expression,
                         expected_eval)


class ReadVarsFromFileTestCase(unittest.TestCase):
    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.db = DatabaseWriter(TEST_DB_NAME)

        with open("test_file.txt",  'w') as fp:
            fp.writelines((
                "RULE some rule\n",
                "not a RULE\n",
                "VAR parrot int\n",
                "vAr ANT float\n",
                "rule\n"
            ))

    def test_read_vars_from_file(self):
        read_vars_form_file("test_file.txt", self.db)

        result = self.db.variables
        expected = (Variable(int, "parrot"), Variable(float, "ant"))

        self.assertTupleEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
