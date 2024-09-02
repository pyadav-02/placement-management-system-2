import sqlite3
import os
project_directory = os.path.dirname(os.path.abspath(__file__))
ADDRESS = os.path.join(project_directory, 'database.db')

connection = sqlite3.connect(ADDRESS)
cursor = connection.cursor()
print('connected')


def execute_query(query, parameters, return_data=False):
    print("*" * 20)
    print(query)
    print(parameters)
    print('*' * 20)

    global cursor
    cursor.execute(query, parameters)

    if return_data:
        return cursor.fetchall()
    else:
        connection.commit()


def disconnect():
    global connection
    connection.close()
