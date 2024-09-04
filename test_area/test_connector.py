import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from utility.connector import Connector


class TestConnector(unittest.TestCase):
    @patch('utility.connector.sqlite3.connect')
    def test_make_connection(self, mock_connect):
        cursor = MagicMock()
        connection = MagicMock()
        connection.cursor = MagicMock(return_value=cursor)
        mock_connect.return_value = connection

        Connector.make_connection()
        mock_connect.assert_called_once_with(Connector.ADDRESS)

    @patch('utility.connector.sqlite3.connect')
    def test_execute_query_true(self, mock_connect):
        mock_cursor = MagicMock()
        connection = MagicMock()
        connection.cursor = MagicMock(return_value=mock_cursor)
        mock_connect.return_value = connection
        Connector.make_connection()

        query = 'select * from student where col1 = ?'
        parameters = ('val1',)

        mock_cursor.fetchall = MagicMock(return_value=[('val1', 'val2', 'val3', 'val4')])
        mock_cursor.execute = MagicMock()

        Connector.execute_query(query, parameters)
        # mock_execute.assert_called_once_with(query, parameters)
        # mock_fetchall.assert_called_once()
        # mock_fetchall.assert_not_called()



