"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021 Lulof Pirée & Edwin Steenkamer

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

Class for organizing a sorf of 'calendar' of sets of recurring questions.
"""
import time
from typing import Set

from robots_everywhere.question_gen.question_occurrence import QuestionOccurrence


class QuestionSchedule:
    # Placeholder!!!
    pass

    def __init__(self, question_sets, prev_timestamp = time.time()):
        self.__prev_timestamp = prev_timestamp

    def get_new_occurences(self,
                           current_time: float = None
                           ) -> Set[QuestionOccurrence]:
        pass
