import unittest
from unittest.mock import patch, call
from business_layer.job import Job
from utility import table_names as tbn


class TestJobFunctionality(unittest.TestCase):
    @patch('business_layer.job.db.insert_record')
    def test_create_job_postings(self, mock_insert_record):
        company_name = 'watchGuard'
        job_description = 'for software role'
        ctc = '12'
        applicable_branches = 'cse, it, ee'
        total_rounds_count = '3'
        application_close_date = '11-09-2024'

        table_name = tbn.JOB_POSTING
        record = dict(company_name=company_name,
                      job_description=job_description,
                      ctc=ctc,
                      applicable_branches=applicable_branches,
                      total_rounds_count=total_rounds_count,
                      current_round='0',
                      application_close_date=application_close_date)

        call_value = (company_name, job_description, ctc, applicable_branches,
                      total_rounds_count, application_close_date)
        Job.create_job_posting(*call_value)

        mock_insert_record.assert_called_once_with(table_name, record)

    @patch('business_layer.job.db.fetch_record_by_condition')
    def test_get_applicable_job_postings(self, mock_fetch_record_by_condition):
        student_id = 's111122223'
        expected_result = [('tcs', 'sde', '6', '2', '10-09-2024', '11', 's111111119', 'cse, it')]

        return_value_fetch1 = [('cse',)]
        return_value_fetch2 = [('watchGuard', 'sde', '10', '3', '09-02-2025',
                                '12', 's111222112, s111122223', 'cse, me, ce'),
                               ('tata steal', 'thermal system', '11', '2', '09-11-2025',
                                '10', 's111122223, s888888889, s119911991', 'me, ee'),
                               ('tcs', 'sde', '6', '2', '10-09-2024', '11', 's111111119', 'cse, it')]

        mock_fetch_record_by_condition.side_effect = [return_value_fetch1, return_value_fetch2]

        result = Job.get_applicable_job_postings(student_id)
        self.assertEqual(result, expected_result)
        self.assertEqual(mock_fetch_record_by_condition.call_count, 2)

        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('branch',)
        condition = dict(student_id=student_id)
        mock_fetch_record_by_condition.assert_any_call(table_name, return_field, condition)

        table_name = tbn.JOB_POSTING
        return_field = ('company_name', 'job_description', 'ctc', 'total_rounds_count',
                        'application_close_date', 'job_id', 'applicants_id', 'applicable_branches')
        condition = dict(current_round='0')
        mock_fetch_record_by_condition.assert_any_call(table_name, return_field, condition)

    @patch('business_layer.job.db.update_record_by_id')
    @patch('business_layer.job.db.fetch_record_by_condition')
    def test_student_apply_for_job_none(self, mock_fetch_record_by_condition, mock_update_record_by_id):
        job_id = '12'
        student_id = 's111111119'

        mock_fetch_record_by_condition.return_value = [('None',)]

        Job.student_apply_for_job(job_id, student_id)

        table_name = tbn.JOB_POSTING
        return_field = ('applicants_id',)
        condition = dict(job_id=job_id)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, condition)

        id_field = 'job_id'
        id_field_value = job_id
        applicants_id = student_id
        updates = dict(applicants_id=applicants_id)
        mock_update_record_by_id.assert_called_once_with(table_name, id_field, id_field_value, updates)

    @patch('business_layer.job.db.update_record_by_id')
    @patch('business_layer.job.db.fetch_record_by_condition')
    def test_student_apply_for_job_not_none(self, mock_fetch_record_by_condition, mock_update_record_by_id):
        job_id = '12'
        student_id = 's111111119'

        fetch_return_value = [('s112233441, s112299221', 's228447118',)]
        mock_fetch_record_by_condition.return_value = fetch_return_value

        Job.student_apply_for_job(job_id, student_id)

        table_name = tbn.JOB_POSTING
        return_field = ('applicants_id',)
        condition = dict(job_id=job_id)
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_field, condition)

        id_field = 'job_id'
        id_field_value = job_id
        applicants_id = fetch_return_value[0][0] + ', ' + student_id
        updates = dict(applicants_id=applicants_id)
        mock_update_record_by_id.assert_called_once_with(table_name, id_field, id_field_value, updates)

    @patch('business_layer.job.db.fetch_record_by_condition')
    def test_get_all_job_posting(self, mock_fetch_record_by_condition):
        fetch_return_value = [('91', 'google', 'sde', '12', 'cse, it', '6', '3',
                               '09-09-2024', 's123123123, s767876567')]
        mock_fetch_record_by_condition.return_value = fetch_return_value

        result = Job.get_all_job_posting()
        self.assertEqual(result, fetch_return_value)

        table_name = tbn.JOB_POSTING
        return_fields = ('job_id', 'company_name', 'job_description', 'ctc', 'applicable_branches',
                         'total_rounds_count', 'current_round', 'application_close_date', 'applicants_id')
        conditions = dict()
        mock_fetch_record_by_condition.assert_called_once_with(table_name, return_fields, conditions)

    @patch('business_layer.job.db.update_record_by_id')
    def test_set_round_job_posting(self, mock_update_record_by_id):
        job_id = '23'
        new_applicants_id = ('s123123141', 's123123331', 's1119991118')
        new_current_round = '3'

        Job.set_round_job_posting(job_id, new_applicants_id, new_current_round)

        table_name = tbn.JOB_POSTING
        id_field = 'job_id'
        id_field_value = job_id
        new_applicants_id = ', '.join(new_applicants_id)
        updates = dict(applicants_id=new_applicants_id, current_round=new_current_round)
        mock_update_record_by_id.assert_called_once_with(table_name, id_field, id_field_value, updates)

    @patch('business_layer.job.db.update_record_by_condition')
    def test_set_students_job_status(self, mock_update_record_by_condition):
        company_name = 'watchGuard'
        students_id = ('s123112121', 's119999110', 's734234282')

        Job.set_students_job_status(company_name, students_id)

        table_name = tbn.STUDENT_ACCOUNT
        updates = dict(company_name=company_name, placement_status='placed')
        conditions = (('student_id', 's123112121'), ('student_id', 's119999110'), ('student_id', 's734234282'))
        mock_update_record_by_condition.assert_called_once_with(table_name, updates, conditions)

    @patch('business_layer.job.db.delete_record_by_id')
    def test_close_job_process(self, mock_delete_record_by_id):
        job_id = '21'

        Job.close_job_process(job_id)

        table_name = tbn.JOB_POSTING
        id_field = 'job_id'
        id_field_value = job_id
        mock_delete_record_by_id.assert_called_once_with(table_name, id_field, id_field_value)

    @patch('business_layer.job.db.insert_record')
    def test_send_message(self, mock_insert_record):
        admin_id = 'a888878791'
        message = 'message writen by admin'
        student_id = ('s111122223', 's999980008', 's191000119')

        Job.send_message(admin_id, message, student_id)

        table_name = tbn.MESSAGE
        record_1 = dict(student_id=student_id[0], message=message, admin_id=admin_id)
        record_2 = dict(student_id=student_id[1], message=message, admin_id=admin_id)
        record_3 = dict(student_id=student_id[2], message=message, admin_id=admin_id)

        expected_calls = [call(table_name, record_1),
                          call(table_name, record_2),
                          call(table_name, record_3)]
        mock_insert_record.assert_has_calls(expected_calls)
