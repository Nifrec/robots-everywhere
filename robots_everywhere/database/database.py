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
from abc import ABC
import os
import sqlite3
import time
from typing import Any, Dict, Union, Optional, Sequence, Tuple
import pandas as pd
import numpy as np
import uuid

import robots_everywhere.settings as settings
from robots_everywhere.settings import TYPE_TO_STR


class Variable:

    def __init__(self, var_type: type, name: str):
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


class Database(ABC):
    def __init__(self, db_file: Optional[str] = None):
        """
        Arguments:
            * db_file: file name plus location of the file where the database
                is stored. 
                If None provided will load the default database file.
                If the file does not yet exist it will be created.
        """
        if db_file is None:
            db_file = settings.DB_FILE_LOCATION

        self._conn = connect_to_db(db_file)

    @property
    def variables(self) -> Tuple[Variable]:
        """
        Get all Variables registered in the loaded database.
        """
        return get_all_vars(self._conn)


class DatabaseReader(Database):

    def get_rows_of_var(self, var: Union[Variable, str]) -> pd.DataFrame:
        """
        Return all the values associated with a certain Variable
        that exists in the database.

        The columns are "value" and "timestamp".
        """
        if isinstance(var, Variable):
            var_name = var.name
        else:
            var_name = var
        query = f"""
        SELECT value, timestamp
        FROM {var_name}
        """
        return pd.read_sql(query, self._conn)

    def get_rows_of_vars(self,
                         vars: Union[Sequence[Variable], Sequence[str]]
                         ) -> Dict[str, np.ndarray]:
        result = dict()
        for var in vars:
            if isinstance(var, Variable):
                var = var.name
            result[var] = np.array(self.get_rows_of_var(var)['value'])
        return result


class DatabaseWriter(DatabaseReader):
    """
    Class providing a simplified interface to interacting 
    with a user's database.
    """

    def create_new_var(self, var: Variable):
        """
        Register a new Variable in the currenly loaded database.
        Creates a new table for this variable.
        """
        add_var(self._conn, var)

    def insert_new_value_of_var(self, var: Variable, new_value: Any,
                                timestamp: Optional[int] = None):
        """
        Insert a new row in the table associated with [var].
        The type of new_value should match [var.var_type].
        The time of entry is also recorded, and can optionally be overridden.
        """
        if timestamp is not None:
            insert_new_var_value(self._conn, var, new_value, timestamp)
        else:
            insert_new_var_value(self._conn, var, new_value)


def connect_to_db(db_file: str = settings.DB_FILE_LOCATION
                  ) -> sqlite3.Connection:
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
    __add_to_variables_table(conn, var)
    __create_table_for_var(conn, var)


def __add_to_variables_table(conn: sqlite3.Connection, var: Variable):
    """
    Add a new Variable entry (as a row) to the 'variables' table.
    """
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


def __create_table_for_var(conn: sqlite3.Connection, var: Variable):
    """
    Create a new table for the given Variable.
    The title of the table will equal the name of the Variable.
    It has two columns: 
        * a 'value' column (whose entries should be of type [var.var_type])
        * a 'timestamp' column (whose entries are int seconds since the epoch)
    """
    value_storage_class = __get_var_storage_class(var)
    query = f"""
    CREATE TABLE {var.name} (
        value {value_storage_class} NOT NULL,
        timestamp INT,
        id INT NOT NULL
    );
    """
    conn.execute(query)
    conn.commit()


def __get_var_storage_class(var: Variable) -> str:
    """
    Get the best matching storage class available in SQLite for 
    the var_type of the given variable.
    """

    if var.var_type == int:
        return "INT"
    elif var.var_type == float:
        return "REAL"
    elif var.var_type == str:
        return "TEXT"
    else:
        return "BLOB"


def get_all_vars(conn: sqlite3.Connection) -> Tuple[Variable]:
    df = pd.read_sql(settings.GET_ALL_VARS_QUERY, conn)
    variables = []
    for row_idx in range(len(df)):
        row = df.loc[row_idx, :]
        variables.append(Variable(eval(row[0]), row[1]))
    return tuple(variables)


def insert_new_var_value(conn: sqlite3.Connection,
                         var: Variable,
                         new_value: Any,
                         timestamp: Optional[int] = int(time.time())):
    """
    In the table associated with variable [var], insert a new row
    (new_value, timestamp).
    The provided variable should exist, and the type of new_value
    must match the type of the Variable.
    """
    if var not in get_all_vars(conn):
        raise RuntimeError(f"Variable {var} not known in database")
    if (timestamp < 0) or not isinstance(timestamp, int):
        raise ValueError(f"Timestamp should be a nonnegative integer")
    if not isinstance(new_value, var.var_type):
        raise ValueError(f"Type of [new_value] does not match variable")

    query = f"""
    INSERT INTO {var.name} (value, timestamp, id)
    VALUES (?, ?, ?)
    """
    conn.execute(query, (new_value, timestamp, time.time_ns()))
    conn.commit()
