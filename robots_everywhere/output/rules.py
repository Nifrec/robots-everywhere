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
from typing import Iterable, Sequence, Set, Tuple, Any, Dict, Sized
from numbers import Number
from collections import namedtuple

from robots_everywhere.message import OutputMessage
from robots_everywhere.database.database import DatabaseReader
ParseResults = namedtuple("ParseResults",
                          ["trigger_expr", "message_expr", "eval_expr", "vars_dict"])

QUANTIFIER_TO_REPLACEMENT = {
    "allbutfirst": "[IDX:]",
    "first": "[:IDX]",
    "last": "[-IDX:]",
    "allbutlast": "[:-IDX]"
}

QUANTIFIER_KEYWORDS = ("allbutfirst", "first", "last", "allbutlast")


class RuleExpression(abc.ABC):
    """
    Class for encapsulating an rule expression, according to rules below,
    and pretending it is a normal function:
    """

    def __init__(self, expression: str, variable_names: Set[str]):
        self.__expression = expression
        self.__variables = variable_names

    @property
    def variable_names(self) -> Set[str]:
        return self.__variables.copy()

    def __call__(self, variables_values: Dict[str, np.ndarray]):
        # These two are used as context by self.__expression under this name!
        vars_dict = variables_values
        mean = np.mean

        output = eval(self.__expression)
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
        if isinstance(output, (bool, np.bool_)):
            return True
        elif isinstance(output, np.ndarray) and (len(output) == 1) \
                and isinstance(output[0], np.bool_):
            return True
        else:
            return False


class MessageExpression(RuleExpression):
    """
    Expression that should evaluate to any message.
    Any value except nothing is allowed.
    Here nothing is a length 0 sequence or None.
    """

    def _hook_check_output_value(self, output: Any) -> bool:
        if output is None:
            return False
        elif isinstance(output, Sized) and len(output) == 0:
            return False
        else:
            return True


class EvaluationExpression(RuleExpression):
    """
    Expression that will return a single numeric value in [-1, 1].
    """

    def _hook_check_output_value(self, output: Any) -> bool:
        if isinstance(output, np.ndarray) and len(output) == 1:
            output = output[0]
        elif not isinstance(output, Number):
            return False

        return isinstance(output, Number) and (abs(output) <= 1)


class Rule:

    def __init__(self, trigger: TriggerExpression, messager: MessageExpression,
                 evaluator: EvaluationExpression):
        self.__trigger = trigger
        self.__messager = messager
        self.__evaluator = evaluator
        self.__last_values: Dict[str, tuple] = None

    def check_fireable(self, db: DatabaseReader,
                       record_database_state: bool = False) -> bool:
        """
        Return True if:
            * Any value in the trigger changed in the database 
                since last recorded database state.
            --AND--
            * The trigger holds on the current values in the database.
        """
        var_names = self.__trigger.variable_names
        vars_dict = db.get_rows_of_vars(var_names)

        if self.__last_values == vars_dict:
            return False

        if record_database_state:
            self.__last_values = vars_dict

        return self.__trigger(vars_dict)

    def fire(self, db: DatabaseReader) -> Tuple[Any, float]:
        """
        Run the rule if it is fireable. 
        If not fireable, a RuntimeError will raised.
        Arguments:
            * db: database providing most recent state of the variables
                used in the rule.
        Returns:
            * Any: computed output of the Rule's MessageExpression.
            * float: computed evaluation of the Rule's EvaluationExpression.
        """
        if not self.check_fireable(db, True):
            raise RuntimeError("Rule is not fireable")
        
        var_names = self.__messager.variable_names.union(
            self.__evaluator.variable_names)
        vars_dict = db.get_rows_of_vars(var_names)
        return self.__messager(vars_dict), self.__evaluator(vars_dict)


def parse_expression(expression: str) -> ParseResults:
    """
    Map a raw rule-expression to Python code,
    where each variable is replaced by a dictionary entry.
    It is assumed that this dictionary is called 'vars_dict',
    and is indexed by the names of the variables. 
    The values are the 1D arrays of values of the Variable.

    For example, if some variable "my_var" occurs in the expression,
    it will be substituted by "vars_dict['my_var']".

    Also quantifiers will be substituted as described in the function
    [substitute_quantifiers].
    """
    vars_dict = extract_vars(expression)
    expression = substitute_vars(expression, vars_dict)
    trigger_expr, message_expr, eval_expr = cut_rule_expression(expression)

    trigger_expr = substitute_quantifiers(trigger_expr)
    message_expr = substitute_quantifiers(message_expr)
    eval_expr = substitute_quantifiers(eval_expr)

    return ParseResults(trigger_expr, message_expr, eval_expr, vars_dict)


def substitute_quantifiers(expression: str) -> str:
    """
    Replaces:
        (allbutlast x) -> [:-x]
        (last x) -> [-x:]
        (first x) -> [:x]
        (allbutfirst x) -> [x:]
    """
    __check_for_invalid_quantifiers(expression)
    __check_for_missing_digit(expression)
    for quantifier in QUANTIFIER_KEYWORDS:
        expression = __replace_single_quantifier_type(expression, quantifier)
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
    regex = r'(?!mean)\([^\)\(]*?\)'
    for match in re.findall(regex, expression):
        quantifier = match[1:-1]  # Remove outer brackets
        quantifier = re.sub(r'\d+', "", quantifier, count=1)  # Remove index
        quantifier = re.sub(r'\s*', "", quantifier)  # Remove whitespaces

        if quantifier not in QUANTIFIER_KEYWORDS:
            raise ValueError("Invalid quantifier")


def __check_for_missing_digit(expression: str):
    """
    Raise a ValueError if the expression does not contain any digit.
    """
    if re.search(r'\d', expression) is None:
        raise ValueError("Quantifier must contain an index")


def __replace_single_quantifier_type(expression: str, quantifier: str) -> str:
    regex = r'\(\s*' + quantifier + r'[\s_a-z]*\d*\s*\)'

    match = re.search(regex, expression)
    while match is not None:
        replacement = __create_replacement_for_quantifier_match(
            match.group(0), quantifier)
        start, end = match.span(0)
        expression = expression[:start] + replacement + expression[end:]

        match = re.search(regex, expression)
    return expression


def __create_replacement_for_quantifier_match(match: str, quantifier: str) -> str:
    index = re.search(r'\d+', match).group(0)
    replacement = re.sub("IDX", str(index),
                         QUANTIFIER_TO_REPLACEMENT[quantifier])
    return replacement


def substitute_vars(expression: str, vars_dict: Set[str]):
    """
    Surround each occurence of each element "x" in [vars_dict]
    in [expression] as "vars_dict['x']"
    """
    for var in vars_dict:
        expression = re.sub(var, f"vars_dict['{var}']", expression)
    return expression


def extract_vars(expression: str) -> Set[str]:
    """
    Extract variable names from an expression.
    Variable names should be [a-z_]*
    """
    expression = re.sub(r'mean|first|allbut|last|tanh', " ", expression)
    results = set(re.findall(r'[a-z_]*', expression)).difference(("",))
    return results


def cut_rule_expression(expression: str) -> Tuple[str, str, str]:
    """
    Given a string "rule [1...] | [2...] | [3...]" 
    where [1...], [2...] and [3...]
    are any substrings not containing "rule" or "|",
    with leading and trailing whitespaces removed,
    returns "[1...]", "[2...]" and "tanh([3...])".

    If the last part, i.e. the substring "| [3...]" is not present,
    the value "0" will be substituted for "tanh([3...])".
    """
    expression = expression.lower().strip()
    if expression[:4] != "rule":
        raise ValueError("Invalid rule: does not contain substring 'rule'")
    if "|" not in expression:
        raise ValueError("Invalid rule: does not contain substring '|'")

    expression = expression[4:]
    results = expression.split("|")
    results = tuple(map(lambda x: x.strip(), results))

    if len(results) not in (2, 3) or any((len(x) == 0 for x in results)):
        raise ValueError("Invalid rule")

    if len(results) == 2:
        results = results + ("0",)
    else:
        results = results[:2] + (f"tanh({results[2]})",)

    return results
