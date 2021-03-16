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
import unittest
from robots_everywhere.startup.rule_loading import extract_lines_with_prefix_from_file


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

if __name__ == "__main__":
    unittest.main()

    