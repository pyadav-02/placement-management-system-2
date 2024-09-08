from business_layer.student import Student
from business_layer.job import Job
from utility import validation_utils as valid


class StudentInterface:
    def __init__(self, student_object: Student):
        self.student = student_object

    @staticmethod
    def student_create_account():
        student_id, go_back = valid.create_account_id('student')
        if go_back:
            return

        try:
            verification_result = Student.is_account_exist(student_id)
        except Exception:
            print('---a problem has occurred while creating account please try again later---')
            return

        if verification_result:
            print('-----account already exist-----')
            return

        password, go_back = valid.get_password()
        if go_back:
            return

        name, go_back = valid.get_name('Enter your name: ')
        if go_back:
            return

        branch = valid.get_branch()

        year, go_back = valid.get_year()
        if go_back:
            return

        cgpa, go_back = valid.get_cgpa()
        if go_back:
            return

        try:
            Student.create_account_request(student_id, password, name, branch, year, cgpa)
        except Exception:
            print('---a problem has occurred while creating account please try again later---')
            return
        print('-----request for account creation is sent------')

    MENU = """
    press 1 to ask question
    press 2 to view responses of questions
    press 3 to apply for job
    press 4 to view all messages
    press 5 to logout
    """

    def do_student_functions(self):
        print(StudentInterface.MENU)
        choices = (1, 2, 3, 4, 5)
        choice = valid.get_choice(choices)

        while choice != 5:
            if choice == 1:
                self.ask_question()
            elif choice == 2:
                self.view_question_response()
            elif choice == 3:
                self.apply_for_job()
            elif choice == 4:
                self.view_mass_message()

            print(StudentInterface.MENU)
            choice = valid.get_choice(choices)

    def ask_question(self):
        question = input('Enter question: ')
        try:
            self.student.post_question(question)
        except Exception:
            print('---a problem has occurred while posting question please try again later---')

    def view_question_response(self):
        try:
            responses = self.student.get_question_response()
        except Exception:
            print('---a problem has occurred while collecting answers of question please try again later---')
            return

        if len(responses) == 0:
            print('-----you have not asked any questions-----')
            return

        print('-' * 10)
        for response in responses:
            if response[3] == 'true':
                print('question:', response[0])
                print('answered by', response[1])
                print('answer:', response[2])
            elif response[3] == 'false':
                print('question: ', response[0])
                print('---this question is not answered yet---')
            print('-' * 10)

    def apply_for_job(self):
        try:
            job_postings = Job.get_applicable_job_postings(self.student.student_id)
        except Exception:
            print('---a problem has occurred while collecting job details please try again later---')
            return

        if len(job_postings) == 0:
            print('-----no job posting is available-----')
            return

        attribute_names = ('company name:', 'job description:', 'ctc(lpa):', 'total rounds: ',
                           'application closing date:')

        for i in range(len(job_postings)):
            print('-' * 10)
            print(f'press {i + 1} to chose below job posting\n')

            for j in range(len(attribute_names)):
                print(attribute_names[j], job_postings[i][j])

        print('-' * 10)

        menu = """
    press 1 to apply for a job posting
    press 2 to go back
        """

        action_choices = (1, 2)
        all_job_choices = tuple(i + 1 for i in range(len(job_postings)))
        left_job_choices = list(all_job_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        while action_choice != 2:
            input_string = 'Enter input to choose job posting: '
            warning_string = 'invalid option: you have already applied for this job'
            job_choice = valid.get_one_time_choice(all_job_choices, left_job_choices,
                                                   input_string, warning_string)

            job_id = job_postings[job_choice-1][-3]
            try:
                Job.student_apply_for_job(job_id, self.student.student_id)
            except Exception:
                print('---a problem has occurred while applying for job please try again later---')
                return

            company_name = job_postings[job_choice-1][0]
            print(f'-----applied for {company_name}-----')

            if len(left_job_choices) == 0:
                print('-----action on all job postings are taken-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)

    def view_mass_message(self):
        try:
            messages = self.student.get_messages()
        except Exception:
            print('---a problem has occurred while collecting all messages please try again later---')
            return

        if len(messages) == 0:
            print('---no messages---')
            return

        for message in messages:
            print('-' * 10)
            print('message:', message[0])
            print('admin id:', message[1])
        print('-' * 10)
