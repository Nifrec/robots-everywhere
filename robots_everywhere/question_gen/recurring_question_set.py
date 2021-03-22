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

Class that sets the time when a question occurs
"""

import enum
import datetime
import uuid
from robots_everywhere.question_gen.question import Question
from robots_everywhere.question_gen.question_occurrence import QuestionOccurrence


class WeekDay(enum.Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


class RecurringQuestionSet:

    still_due: bool = True
    timestamp_previous_questions: datetime
    i: int

    def __init__(self, days: {WeekDay}, hour: int, minutes: int, questions: {Question}):
        self.__days = days
        self.__hour = hour
        self.__minutes = minutes
        self.__questions = questions


    @property
    def days(self) -> {WeekDay}:
        return self.__days

    @property
    def hour(self) -> int:
        return self.__hour

    @property
    def minutes(self) -> int:
        return self.__minutes

    @property
    def questions(self) -> {Question}:
        return self.__questions

    def is_due(self, current_datetime: datetime = datetime.datetime.now()) -> bool:
        self.current_datetime = current_datetime
        due_time = current_datetime.replace(hour = self.__hour, minute = self.__minutes)

        if self.timestamp_previous_questions < due_time:
            if current_datetime.weekday() > self.__days[self.i] or current_datetime > due_time and current_datetime.weekday() == self.__days[self.i]:
                self.i = self.i + 1
                return True
            else:
                return False
        else:
            return False

    def generate_questions(self, current_time: datetime = datetime.datetime.now()) -> QuestionOccurrence:
        if self.is_due(current_time):
            self.timestamp_previous_questions = current_time
            return QuestionOccurrence(self.questions, id = uuid.uuid4().int)














