import unittest
from unittest.mock import patch
from utility import validation_utils as valid


class TestValid(unittest.TestCase):
    def setUp(self):
        input_patcher = patch('builtins.input')
        self.mock_input = input_patcher.start()
        print_patcher = patch('builtins.print')
        self.mock_print = print_patcher.start()

    def test_get_choice(self):
        choices = (0, 1, 2, 3)
        self.mock_input.side_effect = ['21', 'fja', '1']

        result = valid.get_choice(choices)

        self.assertEqual(result, 1)
        self.assertEqual(self.mock_input.call_count, 3)

    def test_get_account_id_student(self):
        role = 'student'
        self.mock_input.side_effect = ['s2131', 'h123j', 's111111119']

        result = valid.get_account_id()

        self.assertEqual(result, 's111111119')
        self.assertEqual(self.mock_input.call_count, 3)

    def test_get_account_id_admin(self):
        role = 'admin'
        self.mock_input.side_effect = ['s21mmm31', 'pqr123j', 'a111111119']

        result = valid.get_account_id()

        self.assertEqual(result, 'a111111119')
        self.assertEqual(self.mock_input.call_count, 3)

    def test_get_name(self):
        input_string = 'enter my name: '
        self.mock_input.side_effect = ['abc331', 'i&you', 'rishabh']

        result = valid.get_name(input_string)

        self.assertEqual(result, 'Rishabh')
        self.assertEqual(self.mock_input.call_count, 3)
