"""
Project Robots Everywhere (TU Eindhoven) Q3 2020-2021 Group 8
Copyright (C) 2021  Edwin Steenkamer

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

Class Question that generates a question
"""
from robots_everywhere.database.database import Variable

class Question:

    def __init__(self, content: str, variable: Variable):
        self.__content = content
        self.__variable = variable

    @property
    def content(self) -> str:
        return self.__content

    @property
    def variable(self) -> Variable:
        return self.__variable


    def __repr__(self) -> str:
        return f"Question({repr(self.content)},{repr(self.variable)})"

    def __str__(self) -> str:
        return f"Question({repr(self.variable)}):{self.content}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Question):
            return False
        else:
            return other.content == self.content and other.variable == self.variable
