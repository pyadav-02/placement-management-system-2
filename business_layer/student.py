import utility.table_names as tbn
from utility import utils as db
from utility.validation_utils import hash_password


class StudentFunctionality:
    def __init__(self, student_id):
        self.student_id = student_id

    @staticmethod
    def is_account_request_pending(student_id: str) -> bool:
        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('approval_status',)
        conditions = dict(student_id=student_id)

        records = db.fetch_record_by_condition(table_name, return_field, conditions)
        if len(records) == 0:
            return False

        status = records[0][0]
        if status == 'pending':
            return True
        return False

    @staticmethod
    def create_account_request(student_id: str, password: str, name: str, branch: str, year: str, cgpa: str):
        table_name = tbn.STUDENT_ACCOUNT

        password = hash_password(password)
        record = dict(student_id=student_id,
                      password=password,
                      name=name,
                      branch=branch,
                      year=year,
                      cgpa=cgpa,
                      approval_status='pending',
                      placement_status='unplaced')
        db.insert_record(table_name, record)

    @staticmethod
    def is_account_exist(student_id: str) -> bool:
        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('student_id',)
        conditions = dict(student_id=student_id)

        records = db.fetch_record_by_condition(table_name, return_field, conditions)
        if len(records) > 0:
            return True
        return False

    def post_question(self, question):
        table_name = tbn.QUESTION_ANSWER
        record = dict(student_id=self.student_id, question=question, is_answered='false')
        db.insert_record(table_name, record)

    def get_question_response(self):
        table_name = tbn.QUESTION_ANSWER
        return_field = ('question', 'admin_id', 'answer', 'is_answered')
        condition = dict(student_id=self.student_id)

        records = db.fetch_record_by_condition(table_name, return_field, condition)
        return records
