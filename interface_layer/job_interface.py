from business_layer.job import Job
from utility import validation_utils as valid


class JobInterface:
    @staticmethod
    def post_job():
        company_name, flag = valid.get_name('Enter company name: ')
        job_description = input('Enter job description: ')
        ctc = valid.get_float('Enter ctc(lpa): ')

        applicable_branches = []
        print('add applicable branches')
        menu = """
            press 1 add branches
            press 2 to continue filling other details
            """
        choices = (1, 2)
        choice = 1
        while choice != 2:
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

        try:
            Job.create_job_posting(company_name,
                                   job_description,
                                   ctc,
                                   applicable_branches,
                                   total_rounds_count,
                                   application_close_date)
        except Exception:
            print('---an error has occurred while posting the job please try again later---')
            return

    @staticmethod
    def move_job_next_round(job_manager_id, only_view=False):
        try:
            job_postings = Job.get_all_job_posting()
        except Exception:
            print('---an error has occurred while collecting job details please try again later---')
            return

        if len(job_postings) == 0:
            print('-----no job posting is available-----')
            return

        attribute_names = ('job id:', 'company name:', 'job description:', 'ctc(lpa):', 'applicable branches:',
                           'total rounds:', 'current round:', 'application closing date:', 'applicants id:')

        for i in range(len(job_postings)):
            print('-' * 10)

            if not only_view:
                print(f'press {i + 1} to choose below job posting\n')

            for j in range(1, len(attribute_names)):
                print(attribute_names[j], job_postings[i][j])

        print('-' * 10)

        if only_view:
            return

        menu = """
    press 1 select a job posting
    press 2 go back 
        """
        action_choices = (1, 2)
        all_job_choices = tuple(i + 1 for i in range(len(job_postings)))
        left_job_choices = list(all_job_choices)

        print(menu)
        action_choice = valid.get_choice(action_choices)

        job_postings = [list(job_posting) for job_posting in job_postings]
        while action_choice != 2:
            input_string = 'Enter input to chose job posting: '
            warning_string = 'invalid option: all rounds of this job is completed'
            job_choice = valid.get_one_time_choice(all_job_choices, left_job_choices,
                                                   input_string, warning_string)

            job_id = job_postings[job_choice - 1][0]
            company_name = job_postings[job_choice - 1][1]
            current_round = int(job_postings[job_choice - 1][-3])
            total_rounds_count = int(job_postings[job_choice - 1][-4])

            applicants_id = job_postings[job_choice - 1][-1]
            if applicants_id == 'None':
                try:
                    Job.close_job_process(job_id)
                except Exception:
                    print('---an error has occurred while closing job please try again later---')
                    return
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
                    try:
                        Job.set_round_job_posting(job_id, selected_applicants_id, new_current_round)
                    except Exception:
                        print('---an error has occurred while moving job process to next round'
                              ' please try again later---')
                        return

                    message = input('Enter message for selected students: ')
                    try:
                        Job.send_message(job_manager_id, message, selected_applicants_id)
                    except Exception:
                        print('---an error has occurred while sending message---')

                    job_postings[job_choice - 1][-1] = ', '.join(selected_applicants_id)
                    job_postings[job_choice - 1][-3] = new_current_round

                else:
                    try:
                        Job.close_job_process(job_id)
                    except Exception:
                        print('---an error has occurred while closing job process try again later---')
                        return
                    print('---no student had cleared this round---')

            elif current_round == total_rounds_count:
                selected_applicants_id = valid.get_selected_applicants(applicants_id, not_last_round=False)
                if len(selected_applicants_id) != 0:
                    try:
                        Job.set_students_job_status(company_name, selected_applicants_id)
                    except Exception:
                        print('---an error has occurred while updating job process process try again later---')
                        return

                    message = input('Enter message for selected students: ')
                    try:
                        Job.send_message(job_manager_id, message, selected_applicants_id)
                    except Exception:
                        print('---an error has occurred while sending message---')

                try:
                    Job.close_job_process(job_id)
                except Exception:
                    print('---an error has occurred while closing job process try again later---')
                    return

                print('---job process completed---')

            if len(left_job_choices) == 0:
                print('-----process of all jobs are completed-----')
                break

            print(menu)
            action_choice = valid.get_choice(action_choices)
