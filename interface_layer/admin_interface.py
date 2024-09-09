from business_layer.admin import Admin
from utility import validation_utils as valid
from interface_layer.job_interface import JobInterface


class AdminInterface:
    def __init__(self, admin_object: Admin):
        self.admin = admin_object

    MENU = """
    press 1 to approve or refuse accounts
    press 2 to give response of student's questions
    press 3 to post job
    press 4 to view all postings
    press 5 to shift the round of a job to next round
    press 6 to logout
    """

    def do_admin_functions(self):
        print(AdminInterface.MENU)
        choices = (1, 2, 3, 4, 5, 6)
        choice = valid.get_choice(choices)

        while choice != 6:
            if choice == 1:
                self.approve_refuse_accounts()
            elif choice == 2:
                self.give_answer_to_students()
            elif choice == 3:
                JobInterface.post_job()
            elif choice == 4:
                JobInterface.move_job_next_round(self.admin.admin_id, only_view=True)
            elif choice == 5:
                JobInterface.move_job_next_round(self.admin.admin_id)

            print(AdminInterface.MENU)
            choice = valid.get_choice(choices)

    def approve_refuse_accounts(self):
        try:
            account_requests = Admin.get_unapproved_account()
        except Exception:
            print('---a problem has occurred while collecting unapproved requests please try again later---')
            return

        if len(account_requests) == 0:
            print('-----no pending requests-----')
            return

        field_names = ('student id:', 'name:', 'branch:', 'year:')
        for i in range(len(account_requests)):
            print('-' * 10)
            print(f'press {i+1} to choose below account\n')

            for j in range(len(field_names)):
                print(field_names[j], account_requests[i][j])

        print('-' * 10)

        menu = """
    press 1 to approve account
    press 2 to refuse account
    press 3 to go back
        """

        action_choices = (1, 2, 3)
        all_account_choices = tuple(i+1 for i in range(len(account_requests)))
        left_account_choices = list(all_account_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        while action_choice != 3:
            input_string = 'Enter input to choose account: '
            warning_string = 'invalid option: account already chosen once'
            account_choice = valid.get_one_time_choice(all_account_choices,
                                                       left_account_choices,
                                                       input_string,
                                                       warning_string)
            account_id = account_requests[account_choice-1][0]

            if action_choice == 1:

                try:
                    self.admin.approve_account_by_id(account_id)
                    Admin.put_id_in_credentials(account_id)
                except Exception:
                    print('---a problem has occurred while approving requests please try again later---')
                    return
                print('-----account approved-----')

            elif action_choice == 2:
                try:
                    Admin.refuse_account_by_id(account_id)
                except Exception:
                    print('---a problem has occurred while refusing requests please try again later---')
                    return
                print('-----account refused-----')

            if len(left_account_choices) == 0:
                print('-----action on every requests is taken-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)

    def give_answer_to_students(self):
        try:
            questions = Admin.get_all_unanswered_questions()
        except Exception:
            print('---a problem has occurred while collecting questions please try again later---')
            return

        if len(questions) == 0:
            print('-----no unanswered question remaining-----')
            return

        attribute_names = ('asked by:', 'question:')

        for i in range(len(questions)):
            print('-' * 10)
            print(f'press {i + 1} to choose below question\n')

            for j in range(len(attribute_names)):
                print(attribute_names[j], questions[i][j])

        print('-' * 10)

        menu = """
    press 1 to answer question
    press 2 to go back
                """

        action_choices = (1, 2)
        all_job_choices = tuple(i + 1 for i in range(len(questions)))
        left_job_choices = list(all_job_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        while action_choice != 2:
            input_string = 'Enter input to choose question: '
            warning_string = 'invalid option: you have already answered this questions'
            question_choice = valid.get_one_time_choice(all_job_choices, left_job_choices,
                                                        input_string, warning_string)

            question_id = questions[question_choice - 1][-1]
            answer = input('Enter answer: ')
            try:
                self.admin.answer_students_question(question_id, answer)
            except Exception:
                print('---a problem has occurred while posting answer please try again later---')
                return
            print('-----question answered-----')

            if len(left_job_choices) == 0:
                print('-----response of every question is given-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)
