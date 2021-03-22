import unittest
from robots_everywhere.question_gen.recurring_question_set import RecurringQuestionSet


class TestRecurringQuestionSet(unittest.TestCase):
    def test_is_due_1(self):
        test1 = RecurringQuestionSet({1,3,5}, 7, 30, {"test", "test1"}).is_due()
        self.assertEqual(test1, False)


if __name__ == '__main__':
    unittest.main()
