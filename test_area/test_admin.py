from unittest.mock import patch
from business_layer.admin import AdminFunctionality
import utility.table_names as tbn


class TestAdminFunctionality:
    def setup_method(self):
        self.admin_id = 'A962820126'
        self.admin_functionality = AdminFunctionality(self.admin_id)

    @patch('utility.utils.fetch_record_by_condition')
    def test_get_unapproved_account(self, mock_fetch_record_by_condition):
        expected_output = [('s111919191', 'abcde', 'cse', '2025'), ('s881188118', 'rishabh', 'it', '2028')]
        mock_fetch_record_by_condition.return_value = expected_output

        result = AdminFunctionality.get_unapproved_account()
        assert result == expected_output

        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('student_id', 'name', 'branch', 'year')
        conditions = dict(approval_status='pending')
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_fields, conditions)

    @patch('utility.utils.update_record_by_id')
    def test_approve_account_by_id(self, mock_update_record_by_id):
        student_id = '12'

        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        id_field_value = student_id
        updates = dict(approval_status='approved', approver_id=self.admin_id)

        self.admin_functionality.approve_account_by_id(student_id)
        mock_update_record_by_id.assert_called_once_with(table_name, id_field, id_field_value, updates)

    @patch('utility.utils.insert_record')
    @patch('utility.utils.fetch_record_by_condition')
    def test_put_id_in_credentials(self, mock_fetch_record_by_condition, mock_insert_record):
        account_id = 'a181818181'

        table_name = tbn.STUDENT_ACCOUNT
        return_fields = ('password',)
        conditions = dict(student_id=account_id)
        fetch_return_value = [('root_password',)]
        mock_fetch_record_by_condition.return_value = fetch_return_value

        AdminFunctionality.put_id_in_credentials(account_id)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_fields, conditions)

        password = fetch_return_value[0][0]
        table_name = tbn.CREDENTIALS
        record = dict(account_id=account_id, password=password, role='student')
        mock_insert_record.assert_called_once_with(table_name, record)

    @patch('utility.utils.delete_record_by_id')
    def test_refuse_account_by_id(self, mock_delete_record_by_id):
        argument_student_id = 's111111111'

        table_name = tbn.STUDENT_ACCOUNT
        id_field = 'student_id'
        id_field_value = argument_student_id

        AdminFunctionality.refuse_account_by_id(argument_student_id)
        mock_delete_record_by_id.assert_called_once_with(table_name, id_field, id_field_value)

    @patch('utility.utils.fetch_record_by_condition')
    def test_get_all_unanswered_questions(self, mock_fetch_record_by_condition):
        table_name = tbn.QUESTION_ANSWER
        return_field = ('student_id', 'question', 'question_id')
        conditions = dict()

        AdminFunctionality.get_all_unanswered_questions()
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, conditions)

    @patch('utility.utils.update_record_by_id')
    def test_answer_students_question(self, mock_update_record_by_id):
        argument_question_id = '123'
        argument_answer = 'watchGuard interview in room number 8.'

        table_name = tbn.QUESTION_ANSWER
        id_field = 'question_id'
        id_field_value = argument_question_id
        updates = dict(answer=argument_answer, admin_id=self.admin_id, is_answered='true')

        self.admin_functionality.answer_students_question(argument_question_id, argument_answer)
        mock_update_record_by_id.assert_called_once_with(table_name, id_field, id_field_value, updates)
