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

Files for setting up a SQLite database, storing and retrieving information.
"""
import os
import sqlite3

import robots_everywhere.settings as settings

TYPE_TO_STR = {
    str: 'str',
    float: 'flaot',
    int: 'int',
    list: 'list',
    tuple: 'tuple',
    set: 'set',
    dict: 'dict'
}

class Variable:

    def __init__(self, var_type:type, name: str):
        self.__name = name
        self.__var_type = var_type

    @property
    def var_type(self) -> type:
        return self.__var_type

    @property
    def name(self) -> str:
        return self.__name


    def __repr__(self) -> str:
        return f"Variable({TYPE_TO_STR[self.var_type]},{repr(self.name)})"
    
    def __str__(self) -> str:
        return f"Var {self.name}: {TYPE_TO_STR[self.var_type]}"

def connect_to_db() -> sqlite3.Connection:
    if not os.path.exists(settings.DB_FILE_LOCATION):
        conn = sqlite3.connect(settings.DB_FILE_LOCATION)
        setup_database(conn)
    else:
        conn = sqlite3.connect(settings.DB_FILE_LOCATION)

def setup_database(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE test_tab (
            some_int INT PRIMARY KEY
        )
        """
    )
    conn.execute(
        """
        INSERT INTO test_tab
        VALUES (10)
        """
    )

connect_to_db()
