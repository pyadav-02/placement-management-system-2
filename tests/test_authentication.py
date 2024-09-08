from unittest.mock import patch
import unittest
from business_layer.authentication import Authentication
from utility import table_names as tbn


class TestAuthentication(unittest.TestCase):

    @patch('business_layer.authentication.is_hash_password_valid')
    @patch('business_layer.authentication.db.fetch_record_by_condition')
    def test_is_credential_valid_true(self, mock_fetch_record, mock_is_hash_password_valid):
        account_id = 'a111111111'
        password = 'root'
        role = 'admin'
        expected_result = True
        mock_fetch_record.return_value = [('hashed root',)]
        mock_is_hash_password_valid.return_value = True

        result = Authentication.is_credential_valid(account_id, password, role)

        self.assertEqual(result, expected_result)
        table_name = tbn.CREDENTIALS
        return_fields = ('password',)
        conditions = dict(account_id=account_id, role=role)
        mock_fetch_record.assert_called_once_with(table_name, return_fields, conditions)
        mock_is_hash_password_valid.assert_called_once_with(password, 'hashed root')

    @patch('business_layer.authentication.is_hash_password_valid')
    @patch('business_layer.authentication.db.fetch_record_by_condition')
    def test_is_credential_valid_false(self, mock_fetch_record, mock_is_hash_password_valid):
        account_id = 'a111111111'
        password = 'root'
        role = 'admin'
        expected_result = False
        mock_fetch_record.return_value = []
        mock_is_hash_password_valid.return_value = False

        result = Authentication.is_credential_valid(account_id, password, role)

        self.assertEqual(result, expected_result)
        table_name = tbn.CREDENTIALS
        return_fields = ('password',)
        conditions = dict(account_id=account_id, role=role)
        mock_fetch_record.assert_called_once_with(table_name, return_fields, conditions)
        mock_is_hash_password_valid.assert_not_called()
