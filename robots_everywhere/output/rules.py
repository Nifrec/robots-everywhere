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

Rules for when and which output should be displayed to the user.
"""
import re
from typing import Set, Tuple

class RuleExpression:
    """
    Class for encapsulating an rule expression, according to rules below,
    and pretending it is a normal function:

    In general, the rule-defining syntax is:

    rule [expression 1] [comparison] [expression_2] | [expression_3]

    Where:

    (1) [expression 1], [expression 2] and [expression 3] are 
        any valid expression, described further below.
    (2) [comparison] is one of ==, >=, <=, > or <, 
        and indicates whether [expression 1] must be equal, 
        equal or greater, equal or smaller, greater or smaller 
        than [expression 2], respectively, for the rule to be satisfied. 

    Expressions contain either Variables, constant numbers or both, and evaluate to a single number. Variables must always be indexed, as they generally speaking have multiple entries. Given a Variable named x, it can be indexed as x([specifier] [num]), where

    [specifier] is one of any, allButLast, last, first, allButFirst
    [num] is an integer. 

    Supported binary operations are +, -, /, * and % 
    (which correspond to the usual arithmetic operations, and % to modulus). 
    The unary operation mean(x(...)) is also supported, 
    with returns the sample mean of a subsequence x(...). 
    """
    def __init__(self, expression: str):
        pass


def parse_expression(expression: str) -> str:
    """
    Map a raw rule-expression to Python code,
    where each variable is replaced by a dictionary entry.
    It is assumed that this dictionary is called 'vars',
    and is indexed by the names of the variables. 
    The values are the 1D arrays of values of the Variable.

    For example, if some variable "my_var" occurs in the expression,
    it will be substituted by "vars['my_var']".
    """
    pass

def extract_vars(expression: str) -> Set[str]:
    """
    Extract variable names from an expression.
    Variable names should be [a-z_]*
    """
    expression = re.sub(r'mean|first|allbut|last', " ", expression)
    results = set(re.findall(r'[a-z_]*', expression)).difference(("",))
    return results


def cut_rule_expression(expression: str) -> Tuple[str, str]:
    """
    Given a string "rule [1...] | [2...]" where [1...] and [2...]
    are any substrings not containing "rule" or "|",
    returns [1...] and [2...].
    """
    expression = expression.lower().strip()
    if expression[:4] != "rule":
        raise ValueError("Invalid rule: does not contain substring 'rule'")
    if "|" not in expression:
        raise ValueError("Invalid rule: does not contain substring '|'")
    
    expression = expression[4:]
    results = expression.split("|")
    results = tuple(map(lambda x: x.strip(), results))

    if len(results) != 2 or any((len(x) == 0 for x in results)):
        raise ValueError("Invalid rule")

    return results

