import unittest
from unittest.mock import patch, MagicMock
from utility import validation_utils as valid


class TestValid(unittest.TestCase):
    def setUp(self):
        self.input_patcher = patch('builtins.input')
        self.mock_input = self.input_patcher.start()
        self.print_patcher = patch('builtins.print')
        self.mock_print = self.print_patcher.start()

    def tearDown(self):
        self.input_patcher.stop()
        self.print_patcher.stop()

    def test_get_choice(self):
        choices = (0, 1, 2, 3)
        self.mock_input.side_effect = ['21', 'fja', '1']

        result = valid.get_choice(choices)

        self.assertEqual(result, 1)
        self.assertEqual(self.mock_input.call_count, 3)

    @patch('utility.validation_utils.get_choice')
    def test_get_account_id(self, mock_get_choice):
        mock_get_choice.side_effect = [1, 1]
        self.mock_input.side_effect = ['s21&31', 'h1*23j', 's118abc']
        expected_result = ('s118abc', False)

        result = valid.get_account_id()

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 3)
        self.assertEqual(mock_get_choice.call_count, 2)

    @patch('utility.validation_utils.get_choice')
    def test_get_account_id_go_back(self, mock_get_choice):
        mock_get_choice.side_effect = [1, 2]
        self.mock_input.side_effect = ['s21&31', 'h1*23j']
        expected_result = ('h1*23j', True)

        result = valid.get_account_id()

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 2)
        self.assertEqual(mock_get_choice.call_count, 2)

    def create_account_id(self, mock_get_choice, role):
        mock_get_choice.side_effect = [1, 1]
        self.mock_input.side_effect = ['abc123', 'a111111', role[0] + '111111111']
        expected_result = (role[0] + '111111111', False)

        result = valid.create_account_id(role)

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 3)
        self.assertEqual(mock_get_choice.call_count, 2)

    def create_account_id_go_back(self, mock_get_choice, role):
        mock_get_choice.side_effect = [1, 1, 2]
        self.mock_input.side_effect = ['abc123', '1234', role[0] + 'a111dad']
        expected_result = (role[0] + 'a111dad', True)

        result = valid.create_account_id(role)

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 3)
        self.assertEqual(mock_get_choice.call_count, 3)

    @patch('utility.validation_utils.get_choice')
    def test_create_account_id_student(self, mock_get_choice):
        self.create_account_id(mock_get_choice, 'student')

    @patch('utility.validation_utils.get_choice')
    def test_create_account_id_admin(self, mock_get_choice):
        self.create_account_id(mock_get_choice, 'admin')

    @patch('utility.validation_utils.get_choice')
    def test_create_account_id_student_go_back(self, mock_get_choice):
        self.create_account_id_go_back(mock_get_choice, 'student')

    @patch('utility.validation_utils.get_choice')
    def test_create_account_id_admin_go_back(self, mock_get_choice):
        self.create_account_id_go_back(mock_get_choice, 'admin')

    @patch('utility.validation_utils.get_choice')
    def test_get_name(self, mock_get_choice):
        input_string = 'enter your name= '
        mock_get_choice.side_effect = [1, 1]
        self.mock_input.side_effect = ['abc123', 'a111111111', 'arun kumar']
        expected_result = ('Arun Kumar', False)

        result = valid.get_name(input_string)

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 3)

    @patch('utility.validation_utils.get_choice')
    def test_get_name_go_back(self, mock_get_choice):
        input_string = 'enter your name= '
        mock_get_choice.side_effect = [1, 1, 2]
        self.mock_input.side_effect = ['abc123', 'a111111111', 'arun+kumar']
        expected_result = ('Arun+kumar', True)

        result = valid.get_name(input_string)

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 3)

    @patch('utility.validation_utils.get_choice')
    def test_get_branch(self, mock_get_choice):
        branches = ('cse', 'it', 'ee', 'me', 'ce')
        mock_get_choice.return_value = 2
        expected_output = branches[1]

        result = valid.get_branch()

        self.assertEqual(result, expected_output)
        mock_get_choice.assert_called_once_with([1, 2, 3, 4, 5])

    def test_is_float_false(self):
        self.assertEqual(valid.is_float('12.r123'), False)
        self.assertEqual(valid.is_float('12.r123.fda'), False)

    def test_is_float_true(self):
        self.assertEqual(valid.is_float('12.123'), True)

    def test_get_float(self):
        self.mock_input.side_effect = ['ah1', '.', '213']
        expected_result = '213'

        result = valid.get_float('enter: ')
        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_print.call_count, 2)

    @patch('utility.validation_utils.get_choice')
    @patch('utility.validation_utils.get_float')
    def test_get_cgpa(self, mock_get_float, mock_get_choice):
        mock_get_float.side_effect = ['12', '19.91', '8.42']
        mock_get_choice.side_effect = [1, 1]
        expected_result = ('8.42', False)

        result = valid.get_cgpa()

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_float.call_count, 3)
        self.assertEqual(mock_get_choice.call_count, 2)

    @patch('utility.validation_utils.get_choice')
    @patch('utility.validation_utils.get_float')
    def test_get_cgpa_go_back(self, mock_get_float, mock_get_choice):
        mock_get_float.side_effect = ['12', '19.91']
        mock_get_choice.side_effect = [1, 2]
        expected_result = ('19.91', True)

        result = valid.get_cgpa()

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_float.call_count, 2)
        self.assertEqual(mock_get_choice.call_count, 2)

    def test_get_integer_input(self):
        self.mock_input.side_effect = ['abc', '12r1', '123']
        expected_result = '123'

        result = valid.get_integer_input('enter: ')

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 3)

    @patch('utility.validation_utils.get_integer_input')
    @patch('utility.validation_utils.get_choice')
    def test_get_year(self, mock_get_choice, mock_get_integer_input):
        mock_get_choice.side_effect = [1, 1]
        mock_get_integer_input.side_effect = [2000, 3000, 2025]
        expected_result = (2025, False)

        result = valid.get_year()

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_choice.call_count, 2)
        self.assertEqual(mock_get_integer_input.call_count, 3)

    @patch('utility.validation_utils.get_integer_input')
    @patch('utility.validation_utils.get_choice')
    def test_get_year_go_back(self, mock_get_choice, mock_get_integer_input):
        mock_get_choice.side_effect = [1, 1, 2]
        mock_get_integer_input.side_effect = [2000, 3000, 9025]
        expected_result = (9025, True)

        result = valid.get_year()

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_choice.call_count, 3)
        self.assertEqual(mock_get_integer_input.call_count, 3)

    @patch('utility.validation_utils.get_integer_input')
    def test_get_one_time_choice(self, mock_get_integer_input):
        all_choices = (1, 2, 3, 4)
        left_choices = [1, 4]
        input_string = 'enter: '
        warning_string = 'invalid warning'
        mock_get_integer_input.side_effect = [17, 2, 3, 2, 4]
        expected_result = 4

        result = valid.get_one_time_choice(all_choices, left_choices, input_string, warning_string)
        self.assertEqual(result, expected_result)
        self.assertEqual(left_choices, [1])
        self.assertEqual(mock_get_integer_input.call_count, 5)

    def test_is_date_valid(self):
        self.assertEqual(valid.is_date_valid('abcd'), False)
        self.assertEqual(valid.is_date_valid('au-aj-abcd'), False)
        self.assertEqual(valid.is_date_valid('1-12-2020'), False)
        self.assertEqual(valid.is_date_valid('01-124-2020'), False)
        self.assertEqual(valid.is_date_valid('01-12-202021'), False)
        self.assertEqual(valid.is_date_valid('00-09-1010'), False)
        self.assertEqual(valid.is_date_valid('01-09-1010'), True)
        self.assertEqual(valid.is_date_valid('01-09-1010', future=True), False)
        self.assertEqual(valid.is_date_valid('01-09-2029', future=True), True)

    @patch('utility.validation_utils.is_date_valid')
    def test_get_date(self, mock_is_date_valid):
        self.mock_input.side_effect = ['abcd', 'ah-eu-abcd', '1-909-9919', '01-09-2029']
        mock_is_date_valid.side_effect = [False, False, False, True]
        expected_result = '01-09-2029'

        result = valid.get_date('enter: ')

        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_input.call_count, 4)
        self.assertEqual(self.mock_print.call_count, 3)
        self.assertEqual(mock_is_date_valid.call_count, 4)

    @patch('utility.validation_utils.get_choice')
    def test_get_selected_students(self, mock_get_choice):
        applicants_id = ('123', '221', '111', '1911')
        mock_get_choice.side_effect = [1, 2, 2, 1]
        expected_result = ('123', '1911')

        result = valid.get_selected_applicants(applicants_id)

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_choice.call_count, 4)

    def test_is_password_strong_false(self):
        self.assertEqual(valid.is_password_strong('waterfall'), False)
        self.assertEqual(valid.is_password_strong('waterfall23'), False)
        self.assertEqual(valid.is_password_strong('waterfall@'), False)
        self.assertEqual(valid.is_password_strong('WaterFall@123'), True)

    @patch('utility.validation_utils.get_choice')
    @patch('utility.validation_utils.is_password_strong')
    def test_get_password(self, mock_is_password_strong, mock_get_choice):
        mock_is_password_strong.side_effect = [False, False, True]
        self.mock_input.side_effect = ['butterfly', 'Butterfly123', 'Butter@1234']
        mock_get_choice.side_effect = [1, 1]
        expected_result = ('Butter@1234', False)

        result = valid.get_password()

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_choice.call_count, 2)
        self.assertEqual(mock_is_password_strong.call_count, 3)
        self.assertEqual(self.mock_input.call_count, 3)

    @patch('utility.validation_utils.get_choice')
    @patch('utility.validation_utils.is_password_strong')
    def test_get_password_go_back(self, mock_is_password_strong, mock_get_choice):
        mock_is_password_strong.side_effect = [False, False, False]
        self.mock_input.side_effect = ['butterfly', 'Butterfly123', 'Butter1234']
        mock_get_choice.side_effect = [1, 1, 2]
        expected_result = ('Butter1234', True)

        result = valid.get_password()

        self.assertEqual(result, expected_result)
        self.assertEqual(mock_get_choice.call_count, 3)
        self.assertEqual(mock_is_password_strong.call_count, 3)
        self.assertEqual(self.mock_input.call_count, 3)

    @patch('utility.validation_utils.bcrypt.gensalt')
    @patch('utility.validation_utils.bcrypt.hashpw')
    def test_get_hashed_password(self, mock_haspw, mock_gensalt):
        password = MagicMock()
        password.encode('utf-8').return_value = "b'123abcd445'"
        mock_haspw.return_value = "b'R00tP@@s'"
        mock_gensalt.return_value = 'salt1234'
        expected_result = 'R00tP@@s'

        result = valid.get_hashed_password(password)

        self.assertEqual(result, expected_result)
        mock_haspw.assert_called_once_with(password.encode('utf-8'), 'salt1234')

    @patch('utility.validation_utils.bcrypt.checkpw')
    def test_is_hashed_password_valid_true(self, mock_checkpw):
        mock_checkpw.return_value = True
        result = valid.is_hash_password_valid('1234', 'abcd')
        self.assertEqual(result, True)

    @patch('utility.validation_utils.bcrypt.checkpw')
    def test_is_hashed_password_valid_false(self, mock_checkpw):
        mock_checkpw.return_value = False
        result = valid.is_hash_password_valid('1234', 'abcd')
        self.assertEqual(result, False)
