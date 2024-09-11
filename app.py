from utility.connector import Connector
from interface_layer.main_interface import start_menu


def main():
    try:
        Connector.make_connection()
    except Exception:
        print('We have encountered an error while connecting with database')
        print('-----------------please try again later---------------------')
    else:
        start_menu()
        try:
            Connector.disconnect()
        except Exception:
            pass

    print('\n\n---------------------program ended---------------------------')


if __name__ == '__main__':
    main()
