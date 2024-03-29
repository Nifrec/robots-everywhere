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

Testcases for command.py
"""
from typing import Any
import unittest
from robots_everywhere.database.command import InsertCommand
from robots_everywhere.database.database import DatabaseWriter
from robots_everywhere.database.database import Variable


class MockDatabaseWriter(DatabaseWriter):
    def __init__(self):
        pass

    def insert_new_value_of_var(self, var: Variable, new_value: Any,
                                timestamp: int = None):
        self.input = (var, new_value, timestamp)

    def create_new_var(self, var):
        raise RuntimeError("Should not be called in the tests.")

    def execute_sql_query(self, query, params):
        raise RuntimeError("Should not be called in the tests.")

class InsertCommandTestCase(unittest.TestCase):

    def test_execute(self):
        var = Variable(int, "meh")
        timestamp = 123
        new_value = 321
        id = 999

        db_writer = MockDatabaseWriter()
        command = InsertCommand(db_writer, id, var, new_value, timestamp)
        command.execute()
        
        observation = db_writer.input
        self.assertEqual(observation[0], var)
        self.assertEqual(observation[1], new_value)
        self.assertEqual(observation[2], timestamp)


    def test_undo(self):
        pass

    def test_get_id(self):
        command = InsertCommand(None, 0, None, None)
        self.assertEqual(command.id, 0)

    def test_get_is_executed_1(self):
        """
        After executing a command, its attribute [is_executed] should be True.
        """
        db_writer = MockDatabaseWriter()
        command = InsertCommand(db_writer, 0, Variable(int, "meh"), None)
        command.execute()
        self.assertTrue(command.is_executed)


    def test_get_is_executed_2(self):
        """
        Before executing a command, the attribute [is_executed] should be False.
        """
        command = InsertCommand(None, 0, None, None)
        self.assertFalse(command.is_executed)

if __name__ == "__main__":
    unittest.main()
