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

Script to start-up the full program.
"""
from typing import List, Sequence
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from robots_everywhere.output.output_invoker import OutputInvoker
from robots_everywhere.output.rules import Rule
from robots_everywhere.database.database import DatabaseReader, DatabaseWriter
import robots_everywhere.settings as settings
from robots_everywhere.startup.rule_loading import read_rules_from_file, read_vars_form_file
# from robots_everywhere.gui.motifact_main import MotiFactApp

def start_up():

    print("Starting up MotiFact...")

    db = DatabaseWriter(settings.DB_FILE_LOCATION)
    print("Database loaded.")

    rules = interpret_config_file(db)
    print("Rules and Variables loaded from config file.")
    print("Starting child processes...")
    start_up_child_processes(db, rules)
    print("Child processes started.")

    print("Startup complete.")
    exit()


def interpret_config_file(db: DatabaseWriter,
                          filename=settings.CONFIG_FILE) -> List[Rule]:
    """
    Read the Rules and Variables defined in the config file.
    Add Variables to the provided database,
    and return Rules as a list.
    """
    read_vars_form_file(filename, db)
    return read_rules_from_file(filename)


def start_up_child_processes(db: DatabaseWriter, rules: Sequence[Rule]):
    """
    Start a process for question-generation, output-generation and the GUI.
    """

    gui_to_questions, questions_to_gui = Pipe(duplex=True)
    gui_to_output, output_to_gui = Pipe(duplex=True)

    gui_proc = Process(target=start_up_gui,
                       args=(gui_to_questions, gui_to_output))
    questions_proc = Process(target=start_up_questions,
                             args=(questions_to_gui,))
    output_proc = Process(target=start_up_output_generator,
                          args=(output_to_gui, rules, db))

    gui_proc.start()
    questions_proc.start()
    output_proc.start()


def start_up_gui(conn_to_questions: Connection, conn_to_output: Connection):
    # MotiFactApp().run()
    pass


def start_up_questions(conn_to_gui: Connection):
    pass  # Do something


def start_up_output_generator(conn_to_gui: Connection,
                              rules: Sequence[Rule],
                              database: DatabaseReader):
    output_invoker = OutputInvoker(rules, conn_to_gui, database)
    output_invoker.mainloop(settings.OUTPUT_INVOKER_SLEEP_TIME)


if __name__ == "__main__":
    start_up()
