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

Abstract base class for messages send between processes.
"""
import abc
from typing import Any
from robots_everywhere.database.database import Variable

class Message(abc.ABC):

    def __init__(self, id: int):
        assert isinstance(id, int)
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id

class VariableMessage(Message):
    """
    Message containing a reference to a Variable.
    """

    def __init__(self, id: int, var: Variable):
        super().__init__(id)
        assert isinstance(var, Variable)
        self.__var = var

    @property
    def variable(self) -> Variable:
        return self.__var

class TextMessage():
    """
    Message with a string.
    Can be used to package a text message to send to the user.
    """

    def __init__(self, id: int, text: str):
        super().__init__(id)
        assert isinstance(text, str)
        self.__text = text


    @property
    def text(self) -> str:
        return self.__text

class QuestionMessage(TextMessage, VariableMessage):
    
    def __init__(self, id: int, text: str, var: VariableMessage):
        TextMessage.__init__(id, text)
        VariableMessage.__init__(id, var)

class AnswerMessage(VariableMessage):
    
    def __init__(self, id: int, var: Variable, value: Any):
        super().__init__(id, var)
        self.__value = value
    
    @property
    def value(self) -> Any:
        return self.__value

class OutputMessage(TextMessage):
    """
    Message carrying a text (a string) 
    and an evaluation (a float in [-1, 1]).
    """

    def __init__(self, id: int, text: str, evaluation: float):
        super().__init__(id, text)
        assert isinstance(evaluation, float) and abs(evaluation) <= 1
        self.__eval = evaluation

    @property
    def evaluation(self) -> float:
        return self.__eval
