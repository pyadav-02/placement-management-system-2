import utility.table_names as tbn
from utility import utils as db


class Admin:
    def __init__(self, admin_id):
        self.admin_id = admin_id

    @staticmethod
    def get_unapproved_account() -> list[tuple[str]]:
        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('student_id', 'name', 'branch', 'year')
        conditions = dict(approval_status='pending')

        records = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return records

    def approve_account_by_id(self, student_id: str):
        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        id_field_value = student_id
        updates = dict(approval_status='approved', approver_id=self.admin_id)
        db.update_record_by_id(table_name, id_field, id_field_value, updates)

    @staticmethod
    def put_id_in_credentials(account_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('password',)
        conditions = dict(student_id=account_id)
        records = db.fetch_record_by_condition(table_name, return_fields, conditions)

        password = records[0][0]
        table_name = tbn.CREDENTIALS
        record = dict(account_id=account_id, password=password, role='student')
        db.insert_record(table_name, record)

    @staticmethod
    def refuse_account_by_id(student_id: str):
        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        id_field_value = student_id
        db.delete_record_by_id(table_name, id_field, id_field_value)

    @staticmethod
    def get_all_unanswered_questions():
        table_name = tbn.QUESTION_ANSWER
        return_field = ('student_id', 'question', 'question_id')
        conditions = dict(is_answered='false')
        records = db.fetch_record_by_condition(table_name, return_field, conditions)
        return records

    def answer_students_question(self, question_id, answer):
        table_name = tbn.QUESTION_ANSWER
        id_field = 'question_id'
        id_field_value = question_id
        updates = dict(answer=answer, admin_id=self.admin_id, is_answered='true')
        db.update_record_by_id(table_name, id_field, id_field_value, updates)
