import sqlite3
import os


class Connector:
    project_directory = os.path.dirname(os.path.abspath(__file__))
    ADDRESS = os.path.join(project_directory, 'database.db')

    connection = None
    cursor = None

    @staticmethod
    def make_connection():
        Connector.connection = sqlite3.connect(Connector.ADDRESS)
        Connector.cursor = Connector.connection.cursor()

    @staticmethod
    def execute_query(query, parameters, return_data=False):
        Connector.cursor.execute(query, parameters)

        if return_data:
            return Connector.cursor.fetchall()
        else:
            Connector.connection.commit()

    @staticmethod
    def disconnect():
        Connector.connection.close()
