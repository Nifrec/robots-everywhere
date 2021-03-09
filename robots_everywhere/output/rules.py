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
import abc
import re
import numpy as np
from typing import Iterable, Set, Tuple, Any, Dict, Sized
from collections import namedtuple

ParseResults = namedtuple("ParseResults",
                          ["trigger_expr", "message_expr", "vars"])
REGEX_TO_REPLACEMENT = {
        r'\(\s*allbutfirst[\sa-z]*\d*\s*\)' : "[IDX:]",
        r'\(\s*first[\sa-z]*\d*\s*\)' : "[:IDX]",
        r'\(\s*last[\sa-z]*\d*\s*\)' : "[-IDX:]",
        r'\(\s*allbutlast[\sa-z]*\d*\s*\)' : "[:-IDX]"
    }
QUANTIFIER_KEYWORDS = ("allbutfirst", "first", "last", "allbutlast")

class RuleExpression(abc.ABC):
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

    def __init__(self, expression: str, variables: Set[str]):
        self.__expression = expression
        self.__variables = variables

    @property
    def variables(self) -> Set[str]:
        return self.__variables.copy()

    def __call__(self, variables_values: Dict[str, np.ndarray]):
        vars = variables_values
        mean = np.mean
        output = eval(self.__expression, locals=(vars, mean))
        if not self._hook_check_output_value(output):
            raise RuntimeError(
                "Evaluating rule-expression gave unexpected result")
        return output

    @abc.abstractmethod
    def _hook_check_output_value(self, output: Any) -> bool:
        """
        Method for subclasses to implement:
        return whether the output of __call__ would be
        of desired type.
        """
        pass


class TriggerExpression(RuleExpression):
    """
    Expression that should always evaluate to bools:
    it checks if a rule should be triggered.
    """

    def _hook_check_output_value(self, output: Any) -> bool:
        return isinstance(output, bool)


class MessageExpression(RuleExpression):
    """
    Expression that should evaluate to any message.
    Any value except nothing is allowed.
    Here nothing is a length 0 sequence or None.
    """

    def _hook_check_output_value(self, output: Any) -> bool:
        if output is None:
            return False
        elif issubclass(output, Sized) and len(output) == 0:
            return False
        else:
            return True


def parse_expression(expression: str) -> ParseResults:
    """
    Map a raw rule-expression to Python code,
    where each variable is replaced by a dictionary entry.
    It is assumed that this dictionary is called 'vars',
    and is indexed by the names of the variables. 
    The values are the 1D arrays of values of the Variable.

    For example, if some variable "my_var" occurs in the expression,
    it will be substituted by "vars['my_var']".
    """
    vars = extract_vars(expression)
    expression = substitute_vars(expression, vars)
    trigger_expr, message_expr = cut_rule_expression(expression)
    return ParseResults(trigger_expr, message_expr, vars)

def substitute_quantifiers(expression: str) -> str:
    """
    Replaces:
        (allbutlast x) -> [:-x]
        (last x) -> [-x:]
        (first x) -> [:x]
        (allbutfirst x) -> [x:]
    """
    __check_for_invalid_quantifiers(expression)
    for regex in REGEX_TO_REPLACEMENT.keys():
        expression = __replace_single_quantifier_type(expression, regex)
    return expression

def __check_for_invalid_quantifiers(expression: str): 
    """
    Raise a ValueError if [expression] contains a substring,
    starting and ending with respectively "(" and ")", not prefixed by "mean",
    that does not consist of any single one of the quantifier keywords
    ('first', 'allbutfirst', 'allbutlast' or 'last') followed by a single
    integer.
    Whitespaces are ignored as long as they do not break the keyword or
    the index in multiple separated substrings.
    """
    regex = r'(?!mean)\([\s\w\d]*?\)'
    for match in re.findall(regex, expression):
        quantifier = match[1:-1] # Remove outer brackets
        quantifier = re.sub(r'[1-9]*', "", quantifier) # Remove index
        quantifier = re.sub(r'\s*', "", quantifier) # Remove whitespaces
        
        if quantifier not in QUANTIFIER_KEYWORDS:
            raise ValueError("Invalid quantifier")


def __replace_single_quantifier_type(expression: str, regex: str) -> str:
    for match in re.finditer(regex, expression):
        replacement = __create_replacement_for_quantifier_match(
            match.group(0), regex)
        start, end = match.span(0)
        expression = expression[:start] + replacement + expression[end:]
    return expression

def __create_replacement_for_quantifier_match(match: str, regex: str) -> str:
    index = re.sub(regex[:-11], '', match)
    index = re.sub(regex[-2:], '', index)
    index = eval(index)
    # if not isinstance(index, int):
    #     raise ValueError(f"Int index required, got invalid type: {index}")
    replacement = re.sub("IDX", str(index), REGEX_TO_REPLACEMENT[regex])
    return replacement

def substitute_vars(expression: str, vars: Set[str]):
    """
    Surround each occurence of each element "x" in [vars]
    in [expression] as "vars['x']"
    """
    for var in vars:
        expression = re.sub(var, f"vars['{var}']", expression)
    return expression


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
