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

Collection of settings, such as file names and constants.
"""
import robots_everywhere
import os

# Directory where the robots-everywhere repository is located on the OS.
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(robots_everywhere.__file__))

DB_FILENAME = "robots_db_" + os.getlogin() + ".db"

# Location where the database file (.db) is stored
DB_FILE_LOCATION = os.path.join(PROJECT_ROOT_DIR, DB_FILENAME)