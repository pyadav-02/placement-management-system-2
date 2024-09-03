from unittest.mock import patch
from utility import utils as db


class TestUtils:
    @patch('utility.utils.get_condition_query_string')
    @patch('utility.utils_helper.execute_query')
    def test_fetch_record_by_condition(self, mock_execute_query, mock_get_condition_query_string):
        table_name = 'abc'
        return_fields = ('col1', 'col2', 'col3')
        condition = dict(col1='val1', col2='val2')
        expected_result = [('abc', 'pqr', 'random'), ('123', '456', 'pqr')]

        mock_get_condition_query_string.return_value = 'col1 = ? AND col2 = ? AND 1 = 1'

        result = db.fetch_record_by_condition(table_name, return_fields, condition)
        assert result == expected_result

        # query = ('SELECT col1, col2, col3 '
        #          'FROM abc '
        #          'WHERE col1 = ? AND col2 = ? AND 1 = 1;')
        # parameter = ('val1', 'val2')






