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
from robots_everywhere.database.database import DatabaseWriter, Variable

from typing import List, Sequence
from robots_everywhere.output.rules import Rule, TriggerExpression, \
    MessageExpression, EvaluationExpression, cut_rule_expression, \
        extract_vars, substitute_quantifiers, substitute_vars

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

        trig_vars =  extract_vars(cut_rule[0])
        trig_expr = substitute_vars(cut_rule[0], trig_vars)
        trig_expr = substitute_quantifiers(trig_expr)
        trigger = TriggerExpression(trig_expr, trig_vars)

        mess_vars =  extract_vars(cut_rule[1])
        mess_expr = substitute_vars(cut_rule[1], mess_vars)
        mess_expr = substitute_quantifiers(mess_expr)
        messager = MessageExpression(mess_expr, mess_vars)

        eval_vars =  extract_vars(cut_rule[2])
        eval_expr = substitute_vars(cut_rule[2], eval_vars)
        eval_expr = substitute_quantifiers(eval_expr)
        evaluator = EvaluationExpression(eval_expr, eval_vars)
        rule = Rule(trigger, messager, evaluator)
        output.append(rule)
    return output

def read_vars_form_file(filename: str, db: DatabaseWriter):
    """
    Read all Variable definitions from a file,
    and store any new Variables in the database.
    All cases are converted to lowercase.
    """
    var_lines = extract_lines_with_prefix_from_file(filename, "VAR")
    existing_var_names = tuple(map(lambda x: x.name, db.variables))
    for var_line in var_lines:
        var_line = var_line.lower().split()
        new_var = Variable(eval(var_line[2]), var_line[1])
        if new_var.name not in existing_var_names:
            db.create_new_var(new_var)

    
