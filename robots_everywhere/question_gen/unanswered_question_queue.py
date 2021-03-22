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

Class that queues the unanswered questions
"""

from robots_everywhere.question_gen.question_occurrence import QuestionOccurrence


class UnansweredQuestionQueue:

    def __init__(self, unanswered_questions: {QuestionOccurrence}):
        self.unanswered_questions = unanswered_questions

    def pop_unanswered_question(self) -> QuestionOccurrence:
        return self.unanswered_questions.pop()

    def add_new_occurrences_if_any(self, schedule: QuestionSchedule):
        pass

    def is_empty(self) -> bool:
        if len(self.unanswered_questions) == 0:
            return True
        else:
            return False

