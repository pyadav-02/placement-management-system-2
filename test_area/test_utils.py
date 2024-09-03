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








