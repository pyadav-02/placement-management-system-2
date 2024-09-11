from interface_layer.student_interface import StudentInterface
from business_layer.student import Student
from unittest.mock import patch, call
import unittest


class TestAdminInterface(unittest.TestCase):
    def setUp(self):
        self.input_patcher = patch('builtins.input')
        self.mock_input = self.input_patcher.start()
        self.print_patcher = patch('builtins.print')
        self.mock_print = self.print_patcher.start()

        self.student = Student('s11111111')
        self.student_interface = StudentInterface(self.student)
    def tearDown(self):
        self.input_patcher.stop()
        self.print_patcher.stop()

    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_student_id_back(self, mock_create_account_id):
        mock_create_account_id.return_value = ('a1111^@&***9', True)
        StudentInterface.student_create_account()
        mock_create_account_id.assert_called_once_with('student')

    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_already_exist(self, mock_create_account_id, mock_is_account_exist):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = True

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')

    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_already_exist_error(self, mock_create_account_id, mock_is_account_exist):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.side_effect = [Exception]

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')

    @patch('interface_layer.student_interface.valid.get_password')
    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_password_back(self, mock_create_account_id, mock_is_account_exist,
                                                          mock_get_password):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = False
        mock_get_password.return_value = ('root', True)

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')

    @patch('interface_layer.student_interface.valid.get_name')
    @patch('interface_layer.student_interface.valid.get_password')
    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_name_back(self, mock_create_account_id, mock_is_account_exist,
                                                      mock_get_password, mock_get_name):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = False
        mock_get_password.return_value = ('R00tP@@s', False)
        mock_get_name.return_value = ('jad&81k', True)

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')

    @patch('interface_layer.student_interface.valid.get_year')
    @patch('interface_layer.student_interface.valid.get_branch')
    @patch('interface_layer.student_interface.valid.get_name')
    @patch('interface_layer.student_interface.valid.get_password')
    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_year_back(self, mock_create_account_id, mock_is_account_exist,
                                                      mock_get_password, mock_get_name, mock_get_branch,
                                                      mock_get_year):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = False
        mock_get_password.return_value = ('R00tP@@s', False)
        mock_get_name.return_value = ('ramu', False)
        mock_get_branch.return_value = 'cse'
        mock_get_year.return_value = ('12231', True)

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')

    @patch('interface_layer.student_interface.valid.get_cgpa')
    @patch('interface_layer.student_interface.valid.get_year')
    @patch('interface_layer.student_interface.valid.get_branch')
    @patch('interface_layer.student_interface.valid.get_name')
    @patch('interface_layer.student_interface.valid.get_password')
    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_cgpa_back(self, mock_create_account_id, mock_is_account_exist,
                                                      mock_get_password, mock_get_name, mock_get_branch,
                                                      mock_get_year, mock_get_cgpa):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = False
        mock_get_password.return_value = ('R00tP@@s', False)
        mock_get_name.return_value = ('ramu', False)
        mock_get_branch.return_value = 'cse'
        mock_get_year.return_value = ('2021', False)
        mock_get_cgpa.return_value = ('14.1', True)

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')

    @patch('interface_layer.student_interface.Student.create_account_request')
    @patch('interface_layer.student_interface.valid.get_cgpa')
    @patch('interface_layer.student_interface.valid.get_year')
    @patch('interface_layer.student_interface.valid.get_branch')
    @patch('interface_layer.student_interface.valid.get_name')
    @patch('interface_layer.student_interface.valid.get_password')
    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account_error(self, mock_create_account_id, mock_is_account_exist,
                                                  mock_get_password, mock_get_name, mock_get_branch,
                                                  mock_get_year, mock_get_cgpa, mock_create_account_request):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = False
        mock_get_password.return_value = ('R00tP@@s', False)
        mock_get_name.return_value = ('ramu', False)
        mock_get_branch.return_value = 'cse'
        mock_get_year.return_value = ('2021', False)
        mock_get_cgpa.return_value = ('9.1', False)
        mock_create_account_request.side_effect = [Exception]

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')
        mock_create_account_request.assert_called_once_with('a111111119', 'R00tP@@s', 'ramu', 'cse', '2021', '9.1')

    @patch('interface_layer.student_interface.Student.create_account_request')
    @patch('interface_layer.student_interface.valid.get_cgpa')
    @patch('interface_layer.student_interface.valid.get_year')
    @patch('interface_layer.student_interface.valid.get_branch')
    @patch('interface_layer.student_interface.valid.get_name')
    @patch('interface_layer.student_interface.valid.get_password')
    @patch('interface_layer.student_interface.Student.is_account_exist')
    @patch('interface_layer.student_interface.valid.create_account_id')
    def test_student_create_account_account(self, mock_create_account_id, mock_is_account_exist,
                                            mock_get_password, mock_get_name, mock_get_branch,
                                            mock_get_year, mock_get_cgpa, mock_create_account_request):
        mock_create_account_id.return_value = ('a111111119', False)
        mock_is_account_exist.return_value = False
        mock_get_password.return_value = ('R00tP@@s', False)
        mock_get_name.return_value = ('ramu', False)
        mock_get_branch.return_value = 'cse'
        mock_get_year.return_value = ('2021', False)
        mock_get_cgpa.return_value = ('9.1', False)
        mock_create_account_request.return_value = None

        StudentInterface.student_create_account()

        mock_is_account_exist.assert_called_once_with('a111111119')
        mock_create_account_request.assert_called_once_with('a111111119', 'R00tP@@s', 'ramu', 'cse', '2021', '9.1')

    @patch('interface_layer.student_interface.StudentInterface.view_mass_message')
    @patch('interface_layer.student_interface.StudentInterface.apply_for_job')
    @patch('interface_layer.student_interface.StudentInterface.view_question_response')
    @patch('interface_layer.student_interface.StudentInterface.ask_question')
    @patch('interface_layer.student_interface.valid.get_choice')
    def test_do_functions(self, mock_get_choice, mock_ask_question, mock_view_question_response,
                          mock_apply_for_job, mock_view_mass_message):
        mock_get_choice.side_effect = [1, 2, 3, 4, 5]

        self.student_interface.do_student_functions()

        mock_ask_question.assert_called_once()
        mock_view_question_response.assert_called_once()
        mock_apply_for_job.assert_called_once()
        mock_view_mass_message.assert_called_once()
        self.assertEqual(mock_get_choice.call_count, 5)

    @patch('interface_layer.student_interface.Student.post_question')
    def test_ask_question(self, mock_post_question):
        question = 'what?'
        self.mock_input.return_value = question

        self.student_interface.ask_question()

        mock_post_question.assert_called_once_with(question)

    @patch('interface_layer.student_interface.Student.post_question')
    def test_ask_question_error(self, mock_post_question):
        question = 'what?'
        self.mock_input.return_value = question
        mock_post_question.side_effect = [Exception]

        self.student_interface.ask_question()

        mock_post_question.assert_called_once_with(question)




