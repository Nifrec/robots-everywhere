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
import unittest
import os
import sqlite3
import pandas as pd

from robots_everywhere.database.database_writer import connect_to_db
from robots_everywhere.settings import PROJECT_ROOT_DIR

TEST_DB_NAME = os.path.join(PROJECT_ROOT_DIR, "test_db.db")

class DatabaseTestCase(unittest.TestCase):


    def test_init_db_file_created(self):
        """
        Test if the database file gets created.
        """
        remove_database(TEST_DB_NAME)
        conn = connect_to_db(TEST_DB_NAME)
        self.assertTrue(os.path.exists(TEST_DB_NAME))

    def test_init_db_table_cols(self):
        """
        Test if the table 'variables' gets created and has the right columns.
        """
        remove_database(TEST_DB_NAME)
        conn = connect_to_db(TEST_DB_NAME)
        query = """
        SELECT *
        FROM variables;
        """
        df = pd.read_sql(query, conn)
        output_cols = tuple(df.columns)
        expected_cols = ("var_name", "var_type", "timestamp")
        self.assertTupleEqual(output_cols, expected_cols)

    def test_init_db_table_rows(self):
        """
        Test if the table 'variables' gets created and has no rows yet.
        """
        remove_database(TEST_DB_NAME)
        conn = connect_to_db(TEST_DB_NAME)
        query = """
        SELECT *
        FROM variables;
        """
        df = pd.read_sql(query, conn)
        self.assertEqual(len(df), 0)
        


def remove_database(db_file:str = TEST_DB_NAME):
    """
    Remove any instance of a database created.
    """
    if os.path.exists(db_file):
        os.remove(db_file)

if __name__ == "__main__":
    unittest.main()