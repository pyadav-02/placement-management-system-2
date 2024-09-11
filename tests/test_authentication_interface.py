from interface_layer.authentication_interface import AuthenticationInterface
from unittest.mock import patch
import unittest


class TestAuthenticationInterface(unittest.TestCase):
    def setUp(self):
        self.input_patcher = patch('builtins.input')
        self.mock_input = self.input_patcher.start()
        self.print_patcher = patch('builtins.print')
        self.mock_print = self.print_patcher.start()

    def tearDown(self):
        self.input_patcher.stop()
        self.print_patcher.stop()

    @patch('interface_layer.authentication_interface.getpass.getpass')
    @patch('interface_layer.authentication_interface.Authentication.is_credential_valid')
    def test_is_admin_valid_false(self, mock_is_credential_valid, mock_getpass):
        admin_id = 'a111111119'
        mock_getpass.return_value = 'abcd'
        mock_is_credential_valid.return_value = False
        expected_result = False

        result = AuthenticationInterface.is_admin_valid(admin_id)

        self.assertEqual(result, expected_result)
        mock_is_credential_valid.assert_called_once_with(admin_id, 'abcd', 'admin')

    @patch('interface_layer.authentication_interface.getpass.getpass')
    @patch('interface_layer.authentication_interface.Authentication.is_credential_valid')
    def test_is_admin_valid_true(self, mock_is_credential_valid, mock_getpass):
        admin_id = 'a111111119'
        mock_getpass.return_value = 'abcd'
        mock_is_credential_valid.return_value = True
        expected_result = True

        result = AuthenticationInterface.is_admin_valid(admin_id)

        self.assertEqual(result, expected_result)
        mock_is_credential_valid.assert_called_once_with(admin_id, 'abcd', 'admin')

    @patch('interface_layer.authentication_interface.getpass.getpass')
    @patch('interface_layer.authentication_interface.Authentication.is_credential_valid')
    @patch('interface_layer.authentication_interface.Student.is_account_request_pending')
    def test_is_student_valid_pending(self, mock_is_request_pending, mock_is_credential_valid, mock_getpass):
        student_id = 's111111119'
        mock_getpass.return_value = 'abcd'
        mock_is_request_pending.return_value = True
        expected_result = False

        result = AuthenticationInterface.is_student_valid(student_id)

        self.assertEqual(result, expected_result)
        mock_is_request_pending.assert_called_once_with(student_id)
        mock_is_credential_valid.assert_not_called()

    @patch('interface_layer.authentication_interface.getpass.getpass')
    @patch('interface_layer.authentication_interface.Authentication.is_credential_valid')
    @patch('interface_layer.authentication_interface.Student.is_account_request_pending')
    def test_is_student_valid_false(self, mock_is_request_pending, mock_is_credential_valid, mock_getpass):
        student_id = 's111111119'
        mock_getpass.return_value = 'abcd'
        mock_is_request_pending.return_value = False
        mock_is_credential_valid.return_value = False
        expected_result = False

        result = AuthenticationInterface.is_student_valid(student_id)

        self.assertEqual(result, expected_result)
        mock_is_request_pending.assert_called_once_with(student_id)
        mock_is_credential_valid.assert_called_once_with(student_id, 'abcd', 'student')

    @patch('interface_layer.authentication_interface.getpass.getpass')
    @patch('interface_layer.authentication_interface.Authentication.is_credential_valid')
    @patch('interface_layer.authentication_interface.Student.is_account_request_pending')
    def test_is_student_valid_true(self, mock_is_request_pending, mock_is_credential_valid, mock_getpass):
        student_id = 's111111119'
        mock_getpass.return_value = 'abcd'
        mock_is_request_pending.return_value = False
        mock_is_credential_valid.return_value = True
        expected_result = True

        result = AuthenticationInterface.is_student_valid(student_id)

        self.assertEqual(result, expected_result)
        mock_is_request_pending.assert_called_once_with(student_id)
        mock_is_credential_valid.assert_called_once_with(student_id, 'abcd', 'student')
