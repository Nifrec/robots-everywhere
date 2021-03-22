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

Main module of the output-generating process.
Contains the class OutputInvoker, which keeps track of the Rules
and the database, checks in a when new output should be generated,
and sends new output to the GUI.
"""

import time
from multiprocessing.connection import Connection
from typing import Iterable, Sequence, Tuple
import random
import uuid
from numbers import Number

from robots_everywhere.message import FeedbackMessage
from robots_everywhere.database.database import DatabaseReader
from robots_everywhere.output.rules import Rule


class OutputInvoker:

    def __init__(self,
                 rules: Sequence[Rule],
                 pipe_to_gui: Connection,
                 database: DatabaseReader):
        self.__rules = rules
        self.__pipe = pipe_to_gui
        self.__db = database

    def _find_fireable_rules(self) -> Tuple[Rule]:
        return tuple(filter(lambda x: x.check_fireable(self.__db), self.__rules))

    def mainloop(self, sleep_time: float, max_num_steps: Number = float('inf')):
        step = 0
        while step < max_num_steps:
            step += 1

            fireable_rules = self._find_fireable_rules()
            for rule in fireable_rules:
                message_content, evaluation = rule.fire(self.__db)
                message_id = uuid.uuid4().int # Random unique number
                message = FeedbackMessage(message_id,
                                        str(message_content), 
                                        evaluation)
                self.__pipe.send(message)
                print(f"FeedbackMessage with ID={message_id} send to GUI")

            time.sleep(sleep_time)
        print("OutputInvoker stopped.")
