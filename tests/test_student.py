import unittest
from unittest.mock import patch
from business_layer.student import Student
from utility import table_names as tbn


class TestStudentFunctionality(unittest.TestCase):
    def setUp(self):
        self.student_id = 's111111111'
        self.student = Student(self.student_id)

    def test_is_account_request_pending_empty_list(self):
        self.is_account_request_pending_tester([], False)

    def test_is_account_request_pending_status_pending(self):
        self.is_account_request_pending_tester([('pending',)], True)

    def test_id_account_request_pending_status_not_pending(self):
        self.is_account_request_pending_tester([('approved',)], False)

    @patch('business_layer.student.db.fetch_record_by_condition')
    def is_account_request_pending_tester(self, fetch_return_value, expected_result, mock_fetch_record_by_condition):
        argument_student_id = 's191999999'

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('approval_status',)
        conditions = dict(student_id=argument_student_id)

        mock_fetch_record_by_condition.return_value = fetch_return_value
        result = Student.is_account_request_pending(argument_student_id)

        self.assertEqual(result, expected_result)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, conditions)

    @patch('business_layer.student.valid.get_hashed_password')
    @patch('business_layer.student.db.insert_record')
    def test_create_account_request(self, mock_insert_record, mock_get_hashed_password):
        argument_student_id = 's123123123'
        argument_password = 'root'
        argument_name = 'piyush'
        argument_branch = 'me'
        argument_year = '1231'
        argument_cgpa = '7.1'

        table_name = tbn.STUDENT_ACCOUNT
        hash_password = 'hashed root'
        mock_get_hashed_password.return_value = hash_password
        record = dict(student_id=argument_student_id,
                      password=hash_password,
                      name=argument_name,
                      branch=argument_branch,
                      year=argument_year,
                      cgpa=argument_cgpa,
                      approval_status='pending',
                      placement_status='unplaced')

        Student.create_account_request(argument_student_id,
                                       argument_password,
                                       argument_name,
                                       argument_branch,
                                       argument_year,
                                       argument_cgpa)
        mock_insert_record.assert_called_once_with(table_name, record)
        mock_get_hashed_password.assser_called_once_with(argument_password)

    @patch('business_layer.student.db.fetch_record_by_condition')
    def test_is_account_exist_true(self, mock_fetch_record_by_condition):
        student_id = 's110101010'
        expected_output = True

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('student_id',)
        conditions = dict(student_id=student_id)

        mock_fetch_record_by_condition.return_value = [(student_id,)]
        result = Student.is_account_exist(student_id)
        self.assertEqual(result, expected_output)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, conditions)

    @patch('business_layer.student.db.fetch_record_by_condition')
    def test_is_account_exist_false(self, mock_fetch_record_by_condition):
        student_id = 's110101010'
        expected_output = False

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('student_id',)
        conditions = dict(student_id=student_id)

        mock_fetch_record_by_condition.return_value = []
        result = Student.is_account_exist(student_id)
        self.assertEqual(result, expected_output)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, conditions)

    @patch('business_layer.student.db.insert_record')
    def test_post_question(self, mock_insert_record):
        question = 'what is this?'

        table_name = tbn.QUESTION_ANSWER
        record = dict(student_id=self.student.student_id, question=question, is_answered='false')

        self.student.post_question(question)
        mock_insert_record.assert_called_once_with(table_name, record)

    @patch('business_layer.student.db.fetch_record_by_condition')
    def test_get_question_response(self, mock_fetch_record_by_condition):
        expected_output = [('interview in which room?', 'a292919192', 'room number 8', 'true'),
                           ('give complete information?', 'a111118881', 'given sufficient information', 'true')]

        table_name = tbn.QUESTION_ANSWER
        return_field = ('question', 'admin_id', 'answer', 'is_answered')
        condition = dict(student_id=self.student_id)

        mock_fetch_record_by_condition.return_value = expected_output
        result = self.student.get_question_response()
        self.assertEqual(result, expected_output)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, condition)

    @patch('business_layer.student.db.fetch_record_by_condition')
    def test_get_message(self, mock_fetch_record_by_condition):
        expected_output = [('this is message', 'a122233124'), ('message by admin', 'a123191912')]

        mock_fetch_record_by_condition.return_value = expected_output
        self.student.get_messages()

        table_name = tbn.MESSAGE
        return_field = ('message', 'admin_id')
        condition = dict(student_id=self.student_id)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, condition)
