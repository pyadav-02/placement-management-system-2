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

    @patch('utility.utils.execute_query')
    @patch('utility.utils.get_updates_query_string')
    def test_update_record_by_id(self, mock_get_update_query_string, mock_execute_query):
        table_name = 'abc'
        id_field = 'col1'
        id_field_value = 'val1'
        updates = dict(col2='new_val2', col5='new_val5')

        mock_get_update_query_string.return_value = 'col2 = ?, col5 = ?'
        db.update_record_by_id(table_name, id_field, id_field_value, updates)

        query = 'UPDATE abc SET col2 = ?, col5 = ? WHERE col1 = ?;'
        parameters = ('new_val2', 'new_val5', 'val1')
        mock_execute_query.assert_called_once_with(query, parameters)

    def test_get_update_query_string(self):
        updates = dict(col1='val1', col2='val2', col3='val3')
        expected_result = 'col1 = ?, col2 = ?, col3 = ?'

        result = db.get_updates_query_string(updates)
        self.assertEqual(result, expected_result)

    def test_get_condition_query_tuple_string(self):
        conditions = (('col1', 'val1'), ('col2', 'val2'), ('col3', 'val3'))
        logical_operator = 'OR'
        special_condition = '3 != 3'
        expected_output = '3 != 3 OR col1 = ? OR col2 = ? OR col3 = ?'

        result = db.get_condition_query_tuple_string(conditions, logical_operator, special_condition)
        self.assertEqual(result, expected_output)

    @patch('utility.utils.execute_query')
    def test_update_record_by_condition(self, mock_execute_query):
        table_name = 'abc'
        updates = dict(col1='val1', col2='val2')
        conditions = (('col5', 'val5'), ('col9', 'val9'))

        db.update_record_by_condition(table_name, updates, conditions)

        query = 'UPDATE abc SET col1 = ?, col2 = ? WHERE 1 = 2 OR col5 = ? OR col9 = ?;'
        parameter = ('val1', 'val2', 'val5', 'val9')
        mock_execute_query.assert_called_once_with(query, parameter)

    @patch('utility.utils.execute_query')
    def test_delete_record_by_id(self, mock_execute_query):
        table_name = 'abc'
        id_field = 'col1'
        id_field_value = 'val1'

        db.delete_record_by_id(table_name, id_field, id_field_value)

        query = 'DELETE FROM abc WHERE col1 = ?;'
        parameter = ('val1',)
        mock_execute_query.assert_called_once_with(query, parameter)

    @patch('utility.utils.execute_query')
    @patch('utility.utils.get_column_value_string')
    def test_insert_record(self, mock_get_column_value_string, mock_execute_query):
        table_name = 'pqr'
        record = dict(col1='val1', col2='val2', col3='val3')
        mock_get_column_value_string.return_value = ('col1, col2, col3', '(?, ?, ?)')

        db.insert_record(table_name, record)

        mock_get_column_value_string.assert_called_once_with(record)
        query = 'INSERT INTO pqr col1, col2, col3 VALUES(?, ?, ?);'
        parameter = ('val1', 'val2', 'val3')
        mock_execute_query.assert_called_once_with(query, parameter)

    def test_get_column_value_string(self):
        record = dict(col1='val1', col2='val2', col3='val3')
        expected_result = ('(col1, col2, col3)', '(?, ?, ?)')

        result = db.get_column_value_string(record)
        self.assertEqual(expected_result, result)

