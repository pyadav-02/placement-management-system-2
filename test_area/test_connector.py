import unittest
from unittest.mock import patch, MagicMock
from utility.connector import Connector


class TestConnector(unittest.TestCase):
    @patch('utility.connector.sqlite3.connect')
    def test_make_connection(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor = MagicMock(return_value=mock_cursor)
        mock_connect.return_value = mock_connection

        Connector.make_connection()
        mock_connect.assert_called_once_with(Connector.ADDRESS)

    @patch('utility.connector.Connector.connection')
    @patch('utility.connector.Connector.cursor')
    def test_execute_query_true(self, mock_cursor, mock_connection):
        mock_cursor.execute = MagicMock(return_value=None)
        mock_cursor.fetchall = MagicMock(return_value=[('val1', 'val2', 'val3', 'val4')])
        mock_connection.commit = MagicMock(return_value=None)
        query = 'select * from student where col1 = ?'
        parameters = ('val1',)
        expected_output = [('val1', 'val2', 'val3', 'val4')]

        result = Connector.execute_query(query, parameters, return_data=True)

        self.assertEqual(result, expected_output)
        mock_cursor.fetchall.assert_called_once()
        mock_connection.commit.assert_not_called()

    @patch('utility.connector.Connector.connection')
    @patch('utility.connector.Connector.cursor')
    def test_execute_query_false(self, mock_cursor, mock_connection):
        mock_cursor.execute = MagicMock(return_value=None)
        mock_cursor.fetchall = MagicMock(return_value=[('val1', 'val2', 'val3', 'val4')])
        mock_connection.commit = MagicMock(return_value=None)
        query = 'insert into abc values(?, ?);'
        parameters = ('val1', 'val2')
        expected_output = None

        result = Connector.execute_query(query, parameters, return_data=False)

        self.assertEqual(result, expected_output)
        mock_cursor.fetchall.assert_not_called()
        mock_connection.commit.assert_called_once()

    @patch('utility.connector.Connector.connection')
    def test_disconnect(self, mock_connection):
        mock_connection.close.return_value = None
        Connector.disconnect()
        mock_connection.close.asssert_called_once()
