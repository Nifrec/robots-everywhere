"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021  Edwin Steenkamer

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

Class that regulates the occurrence of questions
"""

from typing import Set
from robots_everywhere.question_gen.question import Question


class QuestionOccurrence:

    def __init__(self, questions: Set[Question], id: int):
        self.__id = id
        self.__questions = questions

    @property
    def id(self) -> int:
        return self.__id

    @property
    def questions(self) -> Question:
        return self.__questions

    def __str__(self) -> str:
        return f"{self.id}: {repr(self.questions.content)}"

















