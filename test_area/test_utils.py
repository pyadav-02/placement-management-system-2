import unittest
from unittest.mock import patch
from utility import utils as db


class TestUtils(unittest.TestCase):
    @patch('utility.utils.get_condition_query_string')
    @patch('utility.utils.execute_query')
    def test_fetch_record_by_condition(self, mock_execute_query, mock_get_condition_query_string):
        table_name = 'abc'
        return_fields = ('col1', 'col2', 'col3')
        condition = dict(col1='val1', col2='val2')
        execute_query_return_value = [(12, 23, 'random'), (123, 456, 'pqr')]
        expected_result = [('12', '23', 'random'), ('123', '456', 'pqr')]

        mock_get_condition_query_string.return_value = 'col1 = ? AND col2 = ? AND 1 = 1'
        mock_execute_query.return_value = execute_query_return_value

        result = db.fetch_record_by_condition(table_name, return_fields, condition)
        self.assertEqual(result, expected_result)

    def test_get_condition_query_string(self):
        conditions = dict(col1='val1', col2='val2', col3='val3')
        logical_operator = 'AND'
        special_condition = '1 = 1'
        expected_result = '1 = 1 AND col1 = ? AND col2 = ? AND col3 = ?'

        result = db.get_condition_query_string(conditions, logical_operator, special_condition)
        self.assertEqual(result, expected_result)

    @patch('utility.utils.get_updates_query_string')
    def test_update_record_by_id(self, mock_get_update_query_string):
        table_name = 'abc'
        id_field = 'col1'
        id_field_value = 'val1'
        updates = dict(col2='new_val2', col5='new_val5')

        mock_get_update_query_string.return_value = 'col2 = new_val2, col5 = '





