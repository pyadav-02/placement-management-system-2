from utility import validation_utils as valid

from interface_layer.authenticate_interface import AuthenticationInterface
from interface_layer.admin_interface import AdminInterface

from interface_layer.student_interface import StudentInterface
from business_layer.admin import AdminFunctionality
from business_layer.student import StudentFunctionality


def start_menu():
    menu = """
    press 0 to exit
    press 1 for admin login
    press 2 for student login
    press 3 for creating student account
    """

    print(menu)
    choices = [0, 1, 2, 3]
    choice = valid.get_choice(choices)

    while choice != 0:
        if choice == 1:
            admin_id = valid.get_account_id('admin')
            if AuthenticationInterface.is_admin_valid(admin_id):
                admin = AdminFunctionality(admin_id)
                admin = AdminInterface(admin)
                admin.do_admin_functions()

        elif choice == 2:
            student_id = valid.get_account_id('student')
            if AuthenticationInterface.is_student_valid(student_id):
                student = StudentFunctionality(student_id)
                student = StudentInterface(student)
                student.do_student_functions()

        elif choice == 3:
            StudentInterface.student_create_account()

        print(menu)
        choice = valid.get_choice(choices)
