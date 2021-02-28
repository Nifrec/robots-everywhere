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

Testcases for class DatabaseWriter and its auxiliary methods
in the file database_writer.py
"""
import time
import unittest
import os
import sqlite3
import pandas as pd
from robots_everywhere import settings

from robots_everywhere.database.database_writer import Variable, connect_to_db, add_var
from robots_everywhere.settings import PROJECT_ROOT_DIR

TEST_DB_NAME = os.path.join(PROJECT_ROOT_DIR, "test_db.db")


class ConnectToDBTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.conn = connect_to_db(TEST_DB_NAME)

    def test_init_db_file_created(self):
        """
        Test if the database file gets created.
        """
        self.assertTrue(os.path.exists(TEST_DB_NAME))

    def test_init_db_table_cols(self):
        """
        Test if the table 'variables' gets created and has the right columns.
        """
        df = get_all_rows_variables(self.conn)
        output_cols = tuple(df.columns)
        expected_cols = ("var_name", "var_type", "timestamp")
        self.assertTupleEqual(output_cols, expected_cols)

    def test_init_db_table_rows(self):
        """
        Test if the table 'variables' gets created and has no rows yet.
        """
        query = """
        SELECT *
        FROM variables;
        """
        df = pd.read_sql(query, self.conn)
        self.assertEqual(len(df), 0)

class GetAllVars(unittest.TestCase):

    def todo(self):
        self.fail("TODO")

class AddVarsTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.conn = connect_to_db(TEST_DB_NAME)

    def test_error_if_var_exists(self):
        """
        Each variable name can be added only once.
        A RuntimeError should be raised if two Variables are added with the
        same name. The type of the Variables does not matter.
        """
        var_1 = Variable(int, "some_var")
        var_2 = Variable(str, "some_var")
        add_var(self.conn, var_1)

        with self.assertRaises(RuntimeError):
            add_var(self.conn, var_2)

    def test_timestamp_correct(self):
        """
        In the database, the timestamp of the moment that the Variable
        was created should be stored.
        It needs to be an epoch time in seconds.
        """
        var = Variable(int, "some_var")
        add_var(self.conn, var)
        df = get_all_rows_variables(self.conn)
        timestamp_now = time.time()
        self.assertLess(timestamp_now - df.loc[0, "timestamp"], 2)

    def test_name_correct(self):
        """
        The database should store the name of a stored Variable.
        """
        var = Variable(int, "some_var")
        add_var(self.conn, var)
        df = get_all_rows_variables(self.conn)
        self.assertEqual(df.loc[0, "var_name"], "some_var")

    def test_type_correct(self):
        """
        The database should store a string representation of the type
        of a Variable.
        """
        var = Variable(int, "some_var")
        add_var(self.conn, var)
        df = get_all_rows_variables(self.conn)
        self.assertEqual(df.loc[0, "var_type"], settings.TYPE_TO_STR[int])


def remove_database(db_file: str = TEST_DB_NAME):
    """
    Remove any instance of a database created.
    """
    if os.path.exists(db_file):
        os.remove(db_file)


def get_all_rows_variables(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Read all rows of the 'variables' table
    in the test-database.
    """
    query = """
    SELECT *
    FROM variables;
    """
    return pd.read_sql(query, conn)


if __name__ == "__main__":
    unittest.main()
