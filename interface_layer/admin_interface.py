from business_layer.admin import AdminFunctionality
from business_layer.job import JobFunctionality
from utility import validation_utils as valid


class AdminInterface:
    def __init__(self, admin_object: AdminFunctionality):
        self.admin = admin_object

    MENU = """
    press 0 to logout
    press 1 to approve or refuse accounts
    press 2 to give response of student's questions
    press 3 to post job
    press 4 to view all postings
    press 5 to shift the round of a job to next round
    """

    def do_admin_functions(self):
        print(AdminInterface.MENU)
        choices = (0, 1, 2, 3, 4, 5)
        choice = valid.get_choice(choices)

        while choice != 0:
            if choice == 1:
                self.approve_refuse_accounts()
            elif choice == 2:
                self.give_answer_to_students()
            elif choice == 3:
                AdminInterface.post_job()
            elif choice == 4:
                self.move_job_next_round(only_view=True)
            elif choice == 5:
                self.move_job_next_round()

            print(AdminInterface.MENU)
            choice = valid.get_choice(choices)

    def approve_refuse_accounts(self):
        account_requests = AdminFunctionality.get_unapproved_account()

        if len(account_requests) == 0:
            print('-----no pending requests-----')
            return

        field_names = ('student id:', 'name:', 'branch:', 'year:')
        for i in range(len(account_requests)):
            print('-' * 10)
            print(f'press {i+1} to chose below account\n')

            for j in range(4):
                print(field_names[j], account_requests[i][j])

        print('-' * 10)

        menu = """
        press 0 to go back
        press 1 to approve account
        press 2 to refuse account
        """

        action_choices = (0, 1, 2)
        all_account_choices = tuple(i+1 for i in range(len(account_requests)))
        left_account_choices = list(all_account_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        while action_choice != 0:
            input_string = 'Enter input to chose account: '
            warning_string = 'invalid option: account already chosen once'
            account_choice = valid.get_one_time_choice(all_account_choices,
                                                       left_account_choices,
                                                       input_string,
                                                       warning_string)
            account_id = account_requests[account_choice-1][0]

            if action_choice == 1:
                self.admin.approve_account_by_id(account_id)
                AdminFunctionality.put_id_in_credentials(account_id)
                print('-----account approved-----')

            elif action_choice == 2:
                AdminFunctionality.refuse_account_by_id(account_id)
                print('-----account refused-----')

            if len(left_account_choices) == 0:
                print('-----action on every requests is taken-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)

    def give_answer_to_students(self):
        questions = AdminFunctionality.get_all_unanswered_questions()

        if len(questions) == 0:
            print('-----no unanswered question remaining-----')
            return

        attribute_names = ('asked by:', 'question:')

        for i in range(len(questions)):
            print('-' * 10)
            print(f'press {i + 1} to chose below question\n')

            for j in range(len(attribute_names)):
                print(attribute_names[j], questions[i][j])

        print('-' * 10)

        menu = """
                press 0 to go back
                press 1 to answer question
                """

        action_choices = (0, 1)
        all_job_choices = tuple(i + 1 for i in range(len(questions)))
        left_job_choices = list(all_job_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        while action_choice != 0:
            input_string = 'Enter input to chose question: '
            warning_string = 'invalid option: you have already answered this questions'
            question_choice = valid.get_one_time_choice(all_job_choices, left_job_choices,
                                                        input_string, warning_string)

            question_id = questions[question_choice - 1][-1]
            answer = input('Enter answer: ')
            self.admin.answer_students_question(question_id, answer)
            print('-----question answered-----')

            if len(left_job_choices) == 0:
                print('-----response of every question is given-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)

    @staticmethod
    def post_job():
        company_name = valid.get_name('Enter company name: ')
        job_description = input('Enter job description: ')
        ctc = valid.get_float('Enter ctc(lpa): ')

        applicable_branches = []
        print('add applicable branches')
        menu = """
        press 0 to continue filling other details
        press 1 add branches
        """
        choices = (0, 1)
        choice = 1
        while choice != 0:
            branch = valid.get_branch()
            if branch in applicable_branches:
                print('--branch already added--')
            else:
                applicable_branches.append(branch)
            print(menu)
            choice = valid.get_choice(choices)

        applicable_branches = ', '.join(applicable_branches)
        print(f'selected branches are {applicable_branches}')

        total_rounds_count = valid.get_integer_input('Enter total number of rounds: ')
        application_close_date = valid.get_date('Enter application close date(dd-mm-yyyy): ')

        JobFunctionality.create_job_posting(company_name,
                                            job_description,
                                            ctc,
                                            applicable_branches,
                                            total_rounds_count,
                                            application_close_date)

    def move_job_next_round(self, only_view=False):
        job_postings = JobFunctionality.get_all_job_posting()

        if len(job_postings) == 0:
            print('-----no job posting is available-----')
            return

        attribute_names = ('job id:', 'company name:', 'job description:', 'ctc(lpa):', 'applicable branches:',
                           'total rounds:', 'current round:', 'application closing date:', 'applicants id:')

        for i in range(len(job_postings)):
            print('-' * 10)

            if not only_view:
                print(f'press {i + 1} to chose below job posting\n')

            for j in range(1, len(attribute_names)):
                print(attribute_names[j], job_postings[i][j])

        print('-' * 10)

        if only_view:
            return

        menu = """
                press 0 go back 
                press 1 select a job posting
                """
        action_choices = (0, 1)
        all_job_choices = tuple(i + 1 for i in range(len(job_postings)))
        left_job_choices = list(all_job_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        job_postings = [list(job_posting) for job_posting in job_postings]
        while action_choice != 0:
            input_string = 'Enter input to chose job posting: '
            warning_string = 'invalid option: all rounds of this job is completed'
            job_choice = valid.get_one_time_choice(all_job_choices, left_job_choices,
                                                   input_string, warning_string)

            job_id = job_postings[job_choice-1][0]
            company_name = job_postings[job_choice-1][1]
            current_round = int(job_postings[job_choice-1][-3])
            total_rounds_count = int(job_postings[job_choice-1][-4])

            applicants_id = job_postings[job_choice-1][-1]
            if applicants_id == 'None':
                JobFunctionality.close_job_process(job_id)
                print('-----no student applied for this job-----')
                print(menu)
                action_choice = valid.get_choice(action_choices)
                continue
            applicants_id = tuple(applicants_id.split(', '))

            if current_round < total_rounds_count:
                selected_applicants_id = valid.get_selected_applicants(applicants_id)
                if len(selected_applicants_id) != 0:
                    left_job_choices.append(job_choice)

                    new_current_round = str(current_round + 1)
                    JobFunctionality.set_round_job_posting(job_id, selected_applicants_id, new_current_round)

                    message = input('Enter message for selected students: ')
                    self.admin.send_message(message, selected_applicants_id)

                    job_postings[job_choice-1][-1] = ', '.join(selected_applicants_id)
                    job_postings[job_choice - 1][-3] = new_current_round

                else:
                    JobFunctionality.close_job_process(job_id)
                    print('---no student had cleared this round---')

            elif current_round == total_rounds_count:
                selected_applicants_id = valid.get_selected_applicants(applicants_id, not_last_round=False)
                if len(selected_applicants_id) != 0:
                    JobFunctionality.set_students_job_status(company_name, selected_applicants_id)
                    message = input('Enter message for selected students: ')
                    self.admin.send_message(message, selected_applicants_id)

                JobFunctionality.close_job_process(job_id)

                print('---job process completed---')

            if len(left_job_choices) == 0:
                print('-----process of all jobs are completed-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)
