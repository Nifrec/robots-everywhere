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

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

def start_up():

    gui_to_questions, questions_to_gui = Pipe(duplex=True)
    gui_to_output, output_to_gui = Pipe(duplex=True)

    gui_proc = Process(target=start_up_gui, args=(gui_to_questions, gui_to_output))
    

    questions_proc = Process(target=start_up_questions, args=(questions_to_gui,))
    output_proc = Process(target=start_up_questions, args=(output_to_gui,))

    gui_proc.start()
    questions_proc.start()
    output_proc.start()


def start_up_gui(conn_to_questions: Connection, conn_to_output: Connection):
    pass # Do something

def start_up_questions(conn_to_gui: Connection):
    pass # Do something

def start_up_output_generator(conn_to_gui: Connection):
    pass # Do something