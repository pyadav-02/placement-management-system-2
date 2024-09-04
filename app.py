from utility.connector import Connector
from interface_layer.main_interface import start_menu

Connector.make_connection()
start_menu()
Connector.disconnect()

print('\n\n-----program ended-----')
