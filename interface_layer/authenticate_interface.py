from business_layer.authentication import Authentication
from business_layer.student import Student
import getpass


class AuthenticationInterface:
    @staticmethod
    def is_admin_valid(admin_id):
        password = getpass.getpass('Enter password: ')

        if not Authentication.is_valid(admin_id, password, 'admin'):
            print('-----incorrect account id or password-----')
            return False

        print('-----login successful-----')
        return True

    @staticmethod
    def is_student_valid(student_id):
        password = getpass.getpass('Enter password: ')

        if Student.is_account_request_pending(student_id):
            print('-----account request is pending-----')
            return False

        if not Authentication.is_valid(student_id, password, 'student'):
            print('-----incorrect account id or password-----')
            return False

        print('-----login successful-----')
        return True
