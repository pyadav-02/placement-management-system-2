from interface_layer import main_interface
from unittest.mock import patch, Mock
import unittest


class TestMainInterface(unittest.TestCase):
    def setUp(self):
        self.input_patcher = patch('builtins.input')
        self.mock_input = self.input_patcher.start()
        self.print_patcher = patch('builtins.print')
        self.mock_print = self.print_patcher.start()

    def tearDown(self):
        self.input_patcher.stop()

    @patch('interface_layer.main_interface.AdminInterface.do_admin_functions')
    @patch('interface_layer.main_interface.StudentInterface.do_student_functions')
    @patch('interface_layer.main_interface.StudentInterface.student_create_account')
    @patch('interface_layer.main_interface.AuthenticationInterface.is_student_valid')
    @patch('interface_layer.main_interface.AuthenticationInterface.is_admin_valid')
    @patch('interface_layer.main_interface.valid.get_account_id')
    @patch('interface_layer.main_interface.valid.get_choice')
    def test_start_menu(self, mock_get_choice, mock_get_account_id,
                        mock_is_admin_valid, mock_is_student_valid, mock_student_create_account,
                        mock_do_student_functions, mock_do_admin_functions):
        mock_get_choice.side_effect = [1, 1, 2, 2, 3, 4]
        mock_get_account_id.side_effect = [('*(ak', True), ('a111111111', False),
                                           ('*fds(ak', True), ('s111111111', False)]

        mock_is_admin_valid.return_value = True
        mock_is_student_valid.return_value = True

        main_interface.start_menu()

        mock_is_admin_valid.assert_called_once_with('a111111111')
        mock_is_student_valid.assert_called_once_with('s111111111')
        mock_do_student_functions.assert_called_once()
        mock_do_admin_functions.assert_called_once()
        mock_student_create_account.assert_called_once()






