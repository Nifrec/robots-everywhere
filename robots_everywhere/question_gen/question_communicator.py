"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021 Lulof Pirée

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

Class encapsulating the mainloop of the question-generating and
answer-saving process.
"""
import time
from multiprocessing.connection import Connection
from typing import Iterable, Sequence, Tuple
import random
import uuid
from numbers import Number

from robots_everywhere.message import QuestionMessage, AnswerMessage
from robots_everywhere.database.database import DatabaseReader
from robots_everywhere.output.rules import Rule
from robots_everywhere.database.command import InsertCommand
from robots_everywhere.question_gen.question_schedule import QuestionSchedule
class QuestionCommunicator:

    def __init__(self,
                 pipe_to_gui: Connection,
                 database: DatabaseReader,
                 schedule: QuestionSchedule):
        self.__pipe = pipe_to_gui
        self.__db = database

    def mainloop(self, sleep_time: float, max_num_steps: Number = float('inf')):
        step = 0
        while step < max_num_steps:
            step += 1
            time.sleep(sleep_time)

    def store_answer(ans: AnswerMessage):
        pass



