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

Class representing an encapsulation of an operation on the SQLite database.
"""
import abc
from typing import List, Tuple, Any, Optional
import time

from robots_everywhere.database.database import DatabaseWriter, Variable


class DBCommand(abc.ABC):

    def __init__(self, db_writer: DatabaseWriter):
        self._db_writer = db_writer
        self.__is_executed = False

    @property
    def is_executed(self) -> bool:
        return self.__is_executed

    @abc.abstractmethod
    def execute(self) -> List[Tuple]:
        self.__is_executed = True


class ReversibleCommand(DBCommand):
    """
    A version of the DBCommand with an undo() method.
    Aside from this method, it also has an id,
    which makes the command more easy to associate with another object.
    """

    def __init__(self, db_writer: DatabaseWriter, id: int):
        super().__init__(db_writer)
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id

    @abc.abstractmethod
    def undo(self):
        pass


class InsertCommand(ReversibleCommand):

    def __init__(self,
                 db_writer: DatabaseWriter,
                 id: int,
                 var: Variable,
                 value: Any,
                 timestamp: Optional[int] = None):
        super().__init__(db_writer, id)
        self.__var = var
        self.__value = value
        if timestamp is not None:
            self.__timestamp = timestamp
        else:
            self.__timestamp = round(time.time())

    @property
    def variable(self) -> Variable:
        return self.__var

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    def execute(self) -> None:
        super().execute()
        self._db_writer.insert_new_value_of_var(self.__var,
                                                 self.__value,
                                                 self.__timestamp)

    def undo(self):
        raise RuntimeError("Undo not yet implemented")
