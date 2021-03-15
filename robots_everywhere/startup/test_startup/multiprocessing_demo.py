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

Example used to show how the multiprocessing module works.
"""

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
import time
import os

def start_up():

    conn_1, conn_2 = Pipe(duplex=True)
    my_list = [1, 2, 3]
    print("Startup id:", id(my_list), "pid:", os.getpid())

    proc_1 = Process(target=my_first_proc, args=(conn_1, my_list))
    proc_2 = Process(target=my_second_proc, args=(conn_2, my_list))

    proc_1.start()
    proc_2.start()


def my_first_proc(conn: Connection, some_list: list):
    some_list[0] = 999
    print("Proc 1 id:", id(some_list), some_list, "pid:", os.getpid())
    for _ in range(10):
        print("🐉")
        time.sleep(1)

    while not conn.poll():
        time.sleep(1)

    received_list = conn.recv()
    print("Proc 1 received from proc 2, id:", id(received_list))

def my_second_proc(conn: Connection, some_list: list):
    some_list[2] = 999
    print("Proc 2 id:", id(some_list), some_list, "pid:", os.getpid())

    for _ in range(10):
        print("🦄")
        time.sleep(1)

    conn.send(some_list)


if __name__ == "__main__":
    start_up()