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
from robots_everywhere.database.database import DatabaseWriter, Variable
import unittest
from robots_everywhere.startup.rule_loading import \
    extract_lines_with_prefix_from_file, read_vars_form_file
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

    