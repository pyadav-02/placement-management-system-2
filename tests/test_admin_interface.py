from interface_layer.admin_interface import AdminInterface
from interface_layer.admin_interface import JobInterface
from business_layer.admin import Admin
from unittest.mock import patch, call
import unittest


class TestAdminInterface(unittest.TestCase):
    def setUp(self):
        self.admin = Admin('a111111111')
        self.admin_interface = AdminInterface(self.admin)
        self.input_patcher = patch('builtins.input')
        self.mock_input = self.input_patcher.start()
        self.print_patcher = patch('builtins.print')
        self.mock_print = self.print_patcher.start()
        self.get_choice_patcher = patch('interface_layer.admin_interface.valid.get_choice')
        self.mock_get_choice = self.get_choice_patcher.start()
        self.get_one_time_choice_patcher = patch('interface_layer.admin_interface.valid.get_one_time_choice')
        self.mock_get_one_time_choice = self.get_one_time_choice_patcher.start()

    def tearDown(self):
        self.input_patcher.stop()
        self.print_patcher.stop()
        self.get_choice_patcher.stop()
        self.get_one_time_choice_patcher.stop()

    @patch('interface_layer.admin_interface.JobInterface.move_job_next_round')
    @patch('interface_layer.admin_interface.JobInterface.post_job')
    @patch('interface_layer.admin_interface.AdminInterface.approve_refuse_accounts')
    @patch('interface_layer.admin_interface.AdminInterface.give_answer_to_students')
    def test_do_admin_function(self, mock_give_answer,
                               mock_approve_refuse, mock_post_job,
                               mock_move_job):
        self.mock_get_choice.side_effect = [1, 2, 3, 4, 5, 6]

        self.admin_interface.do_admin_functions()

        self.assertEqual(self.mock_get_choice.call_count, 6)
        mock_give_answer.assert_called_once()
        mock_approve_refuse.assert_called_once()
        mock_post_job.assert_called_once()
        self.assertEqual(mock_move_job.call_count, 2)
        mock_move_job.assert_has_calls([call(self.admin.admin_id, only_view=True),
                                        call(self.admin.admin_id)])

    @patch('interface_layer.admin_interface.Admin.refuse_account_by_id')
    @patch('interface_layer.admin_interface.Admin.put_id_in_credentials')
    @patch('interface_layer.admin_interface.Admin.approve_account_by_id')
    @patch('interface_layer.admin_interface.Admin.get_unapproved_account')
    def test_approve_refuse_account(self, mock_get_unapproved_account, mock_approve_account,
                                    mock_put_id_in_credentials, mock_refuse_account):
        mock_get_unapproved_account.side_effect = [[('s11112223', 'samir', 'it', '2024'),
                                                   ('s991122341', 'hari', 'cse', '2025'),
                                                   ('s312231123', 'tara', 'me', '2025')]]
        self.mock_get_choice.side_effect = [1, 2, 3]
        self.mock_get_one_time_choice.side_effect = [1, 2]

        self.admin_interface.approve_refuse_accounts()

        mock_approve_account.assert_called_once_with('s11112223')
        mock_put_id_in_credentials.assert_called_once_with('s11112223')
        mock_refuse_account.assert_called_once_with('s991122341')

    @patch('interface_layer.admin_interface.Admin.refuse_account_by_id')
    @patch('interface_layer.admin_interface.Admin.put_id_in_credentials')
    @patch('interface_layer.admin_interface.Admin.approve_account_by_id')
    @patch('interface_layer.admin_interface.Admin.get_unapproved_account')
    def test_approve_refuse_account_no_pending_requests(self, mock_get_unapproved_account, mock_approve_account,
                                                        mock_put_id_in_credentials, mock_refuse_account):
        mock_get_unapproved_account.side_effect = [[]]

        self.admin_interface.approve_refuse_accounts()

        mock_approve_account.assert_not_called()
        mock_put_id_in_credentials.assert_not_called()
        mock_refuse_account.assert_not_called()

    @patch('interface_layer.admin_interface.Admin.get_all_unanswered_questions')
    def test_give_answer_to_students_no_questions(self, mock_get_all_unanswered_questions):
        mock_get_all_unanswered_questions.side_effect = [[]]
        self.admin_interface.give_answer_to_students()
        mock_get_all_unanswered_questions.assert_called_once()

    @patch('interface_layer.admin_interface.Admin.answer_students_question')
    @patch('interface_layer.admin_interface.Admin.get_all_unanswered_questions')
    def test_give_answer_to_students(self, mock_get_all_unanswered_questions, mock_answer_students_question):
        mock_get_all_unanswered_questions.side_effect = [[('s111111113', 'what is it', '3'),
                                                          ('s281111111', 'helo helo', '4'),
                                                          ('s111777777', 'room number?', '5')]]
        self.mock_get_choice.side_effect = [1, 1, 2]
        self.mock_get_one_time_choice.side_effect = [1, 2]
        self.mock_input.side_effect = ['bye', 'number 4']

        self.admin_interface.give_answer_to_students()

        mock_answer_students_question.assert_has_calls([call('3', 'bye'), call('4', 'number 4')])



