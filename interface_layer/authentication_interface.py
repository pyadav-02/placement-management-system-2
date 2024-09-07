from business_layer.authentication import Authentication
from business_layer.student import Student
import getpass


class AuthenticationInterface:
    @staticmethod
    def is_admin_valid(admin_id):
        password = getpass.getpass('Enter password: ')

        try:
            verification_result = Authentication.is_credential_valid(admin_id, password, 'admin')
        except Exception:
            print('---a problem has occurred while verifying credentials please try again---')
            return False

        if not verification_result:
            print('-----incorrect account id or password-----')
            return False

        print('-----login successful-----')
        return True

    @staticmethod
    def is_student_valid(student_id):
        password = getpass.getpass('Enter password: ')

        try:
            verification_result = Student.is_account_request_pending(student_id)
        except Exception:
            print('---a problem has occurred while verifying credentials please try again---')
            return False

        if verification_result:
            print('-----account request is pending-----')
            return False

        try:
            verification_result = Authentication.is_credential_valid(student_id, password, 'student')
        except Exception:
            print('---a problem has occurred while verifying credentials please try again---')
            return False

        if not verification_result:
            print('-----incorrect account id or password-----')
            return False

        print('-----login successful-----')
        return True
