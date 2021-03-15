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
in the file database.py
"""
import time
import unittest
import os
import sqlite3
import pandas as pd
from robots_everywhere import settings

from robots_everywhere.database.database import Variable
from robots_everywhere.database.database import connect_to_db
from robots_everywhere.database.database import add_var
from robots_everywhere.database.database import get_all_vars
from robots_everywhere.database.database import insert_new_var_value
from robots_everywhere.database.database import DatabaseWriter
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


class GetAllVarsTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.conn = connect_to_db(TEST_DB_NAME)

    def test_no_vars_present(self):
        result = get_all_vars(self.conn)
        self.assertEqual(len(result), 0)

    def test_two_vars_present(self):
        var_1 = Variable(int, "some_int")
        var_2 = Variable(str, "some_str")

        add_var(self.conn, var_1)
        add_var(self.conn, var_2)

        result = get_all_vars(self.conn)
        self.assertEqual(len(result), 2)

        self.assertEqual(var_1, result[0])
        self.assertEqual(var_2, result[1])


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

    def test_empty_table_for_var(self):
        """
        A new, empty, table should be created, with the name of the variable.
        The columns should be 'value' and 'timestamp'.
        """
        var = Variable(int, "some_var")
        add_var(self.conn, var)
        expected_cols = ("value", "timestamp")

        query = """
        SELECT *
        FROM some_var;
        """
        df = pd.read_sql(query, self.conn)

        self.assertTupleEqual(tuple(df.columns), expected_cols)
        self.assertEqual(len(df), 0, "Table should be empty")


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


class InsertVariableValueTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.conn = connect_to_db(TEST_DB_NAME)
        self.var = Variable(int, "test_var")
        add_var(self.conn, self.var)

    def test_insert_valid_value(self):
        new_value = 13
        timestamp = 12345
        insert_new_var_value(self.conn, self.var, new_value, timestamp)

        test_query = """
        SELECT value, timestamp
        FROM test_var;
        """

        df = pd.read_sql(test_query, self.conn)

        self.assertEqual(df.loc[0, "value"], new_value)
        self.assertEqual(df.loc[0, "timestamp"], timestamp)

    def test_insert_invalid_value(self):
        """
        Inserting a float as a value in a table of an int Variable
        should raise an error. A ValueError.
        """
        invalid_value = 13.5
        with self.assertRaises(ValueError):
            insert_new_var_value(self.conn, self.var, invalid_value)

    def test_insert_invalid_var_1(self):
        """
        Corner case: giving a Variable instance with the same name as the one
        of the table, but a different type. The input value corresponds to
        this wrong type as well.
        This should still raise an error! (a RuntimeError)
        """
        invalid_value = 13.5
        fake_var = Variable(float, "test_var")
        with self.assertRaises(RuntimeError):
            insert_new_var_value(self.conn, fake_var, invalid_value)

    def test_insert_invalid_var_2(self):
        """
        Corner case: giving a Variable instance with the same name as the one
        of the table, but a different type. Even if the type of the actual
        new value is correct, this should still raise a RuntimeError.
        """
        invalid_value = 13
        fake_var = Variable(float, "test_var")
        with self.assertRaises(RuntimeError):
            insert_new_var_value(self.conn, fake_var, invalid_value)

    def test_invalid_timestamp(self):
        """
        Timestamps must be nonnegative integers.
        Raise a ValueError on negative timestamps.
        """
        new_value = 10
        timestamp = -1
        with self.assertRaises(ValueError):
            insert_new_var_value(self.conn, self.var, new_value, timestamp)

    def test_table_not_exits(self):
        """
        Cannot insert into the table of nonexisting variables!
        Should raise a RuntimeError.
        """
        another_var = Variable(int, "another_var")
        new_value = 10
        with self.assertRaises(RuntimeError):
            insert_new_var_value(self.conn, another_var, new_value)


class DatabaseWriterTestCase(unittest.TestCase):

    def setUp(self):
        remove_database(TEST_DB_NAME)
        self.db = DatabaseWriter(TEST_DB_NAME)

    def test_get_variables_empty(self):
        """
        Base case: no existing variables should return an empty tuple.
        """
        expected = ()
        result = self.db.variables
        self.assertTupleEqual(expected, result)

    def test_get_variables_not_empty(self):
        """
        Base case: two variables in db should return both (in order).
        """
        var_1 = Variable(int, "v1")
        var_2 = Variable(str, "v2")

        self.db.create_new_var(var_1)
        self.db.create_new_var(var_2)

        expected = (var_1, var_2)
        result = self.db.variables
        self.assertTupleEqual(expected, result)

    def test_get_rows_of_var(self):
        """
        Test insert_new_value_of_var() and get_rows_of_var().
        """
        some_var = Variable(int, "some_var")
        self.db.create_new_var(some_var)
        self.db.insert_new_value_of_var(some_var, 10)
        # Pretend this happens a second later!
        self.db.insert_new_value_of_var(some_var, 12, int(time.time()) + 1)
        df = self.db.get_rows_of_var(some_var)
        timestamp = time.time()

        self.assertEqual(df.loc[0, "value"], 10)
        self.assertEqual(df.loc[1, "value"], 12)
        self.assertLess(timestamp - df.loc[0, "timestamp"], 2)
        self.assertLess(timestamp + 1 - df.loc[1, "timestamp"], 2)
        self.assertEqual(len(df), 2)

    def test_insert_valid_with_timestamp(self):
        var = Variable(int, "test_var")
        self.db.create_new_var(var)

        new_value = 13
        timestamp = 12345
        self.db.insert_new_value_of_var(var, new_value, timestamp)

        test_query = """
        SELECT value, timestamp
        FROM test_var;
        """

        df = self.db.get_rows_of_var(var)

        self.assertEqual(df.loc[0, "value"], new_value)
        self.assertEqual(df.loc[0, "timestamp"], timestamp)


if __name__ == "__main__":
    unittest.main()
