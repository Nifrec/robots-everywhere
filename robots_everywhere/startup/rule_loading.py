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

Functions to help loading rules and variables from a text file.
"""
import warnings

from typing import List, Sequence
from robots_everywhere.output.rules import Rule, TriggerExpression, \
    MessageExpression, EvaluationExpression, cut_rule_expression, extract_vars

warnings.warn("read_rules_from_file() not yet tested")

def extract_lines_with_prefix_from_file(filename: str, prefix: str
                                        ) -> Sequence[str]:
    """
    Returns the lines in the file beginning with the given prefix.
    Case insensitive!
    """
    prefix = prefix.lower()
    with open(filename, 'r') as file:
        all_lines = file.readlines()
        output = tuple(
            filter(lambda x: x.lower().startswith(prefix), all_lines))
        return output


def read_rules_from_file(filename: str) -> List[Rule]:
    output = []
    rule_lines = extract_lines_with_prefix_from_file(filename, "RULE")
    for rule_line in rule_lines:
        cut_rule = cut_rule_expression(rule_line)
        trigger = TriggerExpression(cut_rule[0], extract_vars(cut_rule[0]))
        messager = MessageExpression(cut_rule[1], extract_vars(cut_rule[1]))
        evaluator = TriggerExpression(cut_rule[2], extract_vars(cut_rule[2]))
        rule = Rule(trigger, messager, evaluator)
        output.append(rule)
    return output
