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
import time
from typing import Tuple
import pandas as pd

import robots_everywhere.settings as settings
from robots_everywhere.settings import TYPE_TO_STR

class Variable:

    def __init__(self, var_type:type, name: str):
        if var_type not in TYPE_TO_STR.keys():
            raise ValueError(f"Unsupported variable type '{var_type}'")

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Variable):
            return False
        else:
            return other.name == self.name and other.var_type == self.var_type

def connect_to_db(db_file: str = settings.DB_FILE_LOCATION) -> sqlite3.Connection:
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        setup_vars_table(conn)
    else:
        conn = sqlite3.connect(db_file)
    return conn

def setup_vars_table(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE variables (
            var_name INT PRIMARY KEY,
            var_type TEXT NOT NULL,
            timestamp INT NOT NULL 
        )
        """
    )
    conn.commit()

def add_var(conn: sqlite3.Connection, var: Variable):

    if var.name in map(lambda x: x.name, get_all_vars(conn)):
        raise RuntimeError("Variable name already in database")

    timestamp = int(time.time())

    query = """
    INSERT INTO variables
    VALUES (?, ?, ?);
    """
    params = (var.name, TYPE_TO_STR[var.var_type], timestamp)
    conn.execute(query, params)
    conn.commit()

def get_all_vars(conn: sqlite3.Connection) -> Tuple[Variable]:
    df = pd.read_sql(settings.GET_ALL_VARS_QUERY, conn)
    variables = []
    for row_idx in range(len(df)):
        row = df.loc[row_idx, :]
        variables.append(Variable(eval(row[0]), row[1]))
    return tuple(variables)

