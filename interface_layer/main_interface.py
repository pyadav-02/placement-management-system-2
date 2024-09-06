from utility import validation_utils as valid

from interface_layer.authentication_interface import AuthenticationInterface
from interface_layer.admin_interface import AdminInterface

from interface_layer.student_interface import StudentInterface
from business_layer.admin import Admin
from business_layer.student import Student


def start_menu():
    menu = """
    press 0 to exit
    press 1 for admin login
    press 2 for student login
    press 3 for creating student account
    """

    choices = [0, 1, 2, 3]
    choice = -1
    while choice != 0:

        print(menu)
        choice = valid.get_choice(choices)

        if choice == 1:
            admin_id, go_back = valid.get_account_id()
            if go_back:
                continue

            if AuthenticationInterface.is_admin_valid(admin_id):
                admin = Admin(admin_id)
                admin = AdminInterface(admin)
                admin.do_admin_functions()

        elif choice == 2:
            student_id, go_back = valid.get_account_id()
            if go_back:
                continue

            if AuthenticationInterface.is_student_valid(student_id):
                student = Student(student_id)
                student = StudentInterface(student)
                student.do_student_functions()

        elif choice == 3:
            StudentInterface.student_create_account()
