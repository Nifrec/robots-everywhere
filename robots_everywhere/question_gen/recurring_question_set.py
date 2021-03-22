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
from typing import Set, List, Union, Optional
import time

from robots_everywhere.question_gen.question import Question
from robots_everywhere.question_gen.question_occurrence \
    import QuestionOccurrence

SECOND_IN_A_DAY = 24*60*60


class WeekDay(enum.Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


class WeekTimestamp:

    def __init__(self, day: int, hour: int, minute: int):
        self.day = day
        self.hour = hour
        self.minute = minute


class RecurringQuestionSet:

    def __init__(self, days: Set[WeekDay],
                 hour: int, minutes: int,
                 questions: Set[Question],
                 start_time: Optional[Union[float, None]] = None):
        self.__days = days
        self.__hour = hour
        self.__minutes = minutes
        self.__questions = questions

        if start_time is not None:
            self.__prev_timestamp = start_time
        else:
            self.__prev_timestamp = time.time()
        self.__is_still_due = False

    @property
    def days(self) -> Set[WeekDay]:
        return self.__days

    @property
    def hour(self) -> int:
        return self.__hour

    @property
    def minutes(self) -> int:
        return self.__minutes

    @property
    def questions(self) -> Set[Question]:
        return self.__questions

    def is_due(self, current_timestamp: float,
               ) -> bool:

        if self.__is_still_due():
            return True

        elif current_timestamp < self.__prev_timestamp:
            raise RuntimeError("Not allowed to go back in time")

        elif self.__did_a_schedules_timepoint_pass_since_prev_time(current_timestamp):
            self.__is_still_due = True
            return True

        else:
            return False

    def __did_timepoint_pass_since_prev_generate_questions(self,
                                                           current_time: float
                                                           ) -> bool:
        prev_timestamp_rounded_to_week = self.__prev_timestamp % SECOND_IN_A_DAY
        current_time_rounded_to_week = current_time % SECOND_IN_A_DAY
        is_week_later = prev_timestamp_rounded_to_week < current_time_rounded_to_week
        pass

    def generate_questions(self,
                           current_time: Optional[Union[float, None]] = None
                           ) -> QuestionOccurrence:
        if not self.is_due(current_time):
            raise RuntimeError("ReoccurringQuestionSet is not yet due.")

        self.__is_still_due = False
        if current_time is None:
            current_time = time.time()
        self.__prev_timestamp = current_time

        return QuestionOccurrence(self.questions, id=uuid.uuid4().int)
