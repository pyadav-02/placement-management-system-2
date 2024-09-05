from business_layer.authentication import AuthenticationFunctionality
from business_layer.student import StudentFunctionality
import getpass


class AuthenticationInterface:
    @staticmethod
    def is_admin_valid(admin_id):
        password = getpass.getpass('Enter password: ')

        if not AuthenticationFunctionality.is_valid(admin_id, password, 'admin'):
            print('-----incorrect account id or password-----')
            return False

        print('-----login successful-----')
        return True

    @staticmethod
    def is_student_valid(student_id):
        password = getpass.getpass('Enter password: ')

        if StudentFunctionality.is_account_request_pending(student_id):
            print('-----account request is pending-----')
            return False

        if not AuthenticationFunctionality.is_valid(student_id, password, 'student'):
            print('-----incorrect account id or password-----')
            return False

        print('-----login successful-----')
        return True
