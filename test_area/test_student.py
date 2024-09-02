from unittest.mock import patch
from business_layer.student import StudentFunctionality
from utility import table_names as tbn


class TestStudentFunctionality:
    def setup_method(self):
        self.student_id = 's111111111'
        self.student = StudentFunctionality(self.student_id)

    @patch('utility.utils.fetch_record_by_condition')
    def test_is_account_request_pending_empty_record(self, mock_fetch_record_by_condition):
        argument_student_id = 's191999999'
        expected_result = False

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('approval_status',)
        conditions = dict(student_id=argument_student_id)

        mock_fetch_record_by_condition.return_value = []
        result = StudentFunctionality.is_account_request_pending(argument_student_id)

        assert result == expected_result
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, conditions)

    @patch('utility.utils.insert_record')
    def test_create_account_request(self, mock_insert_record):
        argument_student_id = 's123123123'
        argument_password = 'root'
        argument_name = 'piyush'
        argument_branch = 'me'
        argument_year = '1231'
        argument_cgpa = '7.1'

        table_name = tbn.STUDENT_ACCOUNT
        record = dict(student_id=argument_student_id,
                      password=argument_password,
                      name=argument_name,
                      branch=argument_branch,
                      year=argument_year,
                      cgpa=argument_cgpa,
                      approval_status='pending',
                      placement_status='unplaced')

        StudentFunctionality.create_account_request(argument_student_id,
                                                    argument_password,
                                                    argument_name,
                                                    argument_branch,
                                                    argument_year,
                                                    argument_cgpa)
        mock_insert_record.assert_called_once_with(table_name, record)






