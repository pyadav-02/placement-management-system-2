import utility.table_names as tbn
from utility import utils as db


class Job:
    @staticmethod
    def create_job_posting(company_name,
                           job_description,
                           ctc,
                           applicable_branches: str,
                           total_rounds_count,
                           application_close_date: str):
        table_name = tbn.JOB_POSTING
        record = dict(company_name=company_name,
                      job_description=job_description,
                      ctc=ctc,
                      applicable_branches=applicable_branches,
                      total_rounds_count=total_rounds_count,
                      current_round='0',
                      application_close_date=application_close_date)
        db.insert_record(table_name, record)

    @staticmethod
    def get_applicable_job_postings(student_id):
        table_name = tbn.STUDENT_ACCOUNT
        return_field = ('branch',)
        condition = dict(student_id=student_id)

        branch = db.fetch_record_by_condition(table_name, return_field, condition)
        branch = branch[0][0]

        table_name = tbn.JOB_POSTING
        return_field = ('company_name', 'job_description', 'ctc', 'total_rounds_count',
                        'application_close_date', 'job_id', 'applicants_id', 'applicable_branches')
        condition = dict(current_round='0')

        job_postings = db.fetch_record_by_condition(table_name, return_field, condition)
        applicable_job_postings = []

        for job_posting in job_postings:
            applicable_branches = job_posting[-1].split(', ')
            applicants_id = job_posting[-2].split(', ')

            if branch in applicable_branches and student_id not in applicants_id:
                applicable_job_postings.append(job_posting)

        return applicable_job_postings

    @staticmethod
    def student_apply_for_job(job_id, student_id):
        table_name = tbn.JOB_POSTING
        return_field = ('applicants_id',)
        condition = dict(job_id=job_id)

        applicants_id = db.fetch_record_by_condition(table_name, return_field, condition)
        applicants_id = applicants_id[0][0]

        if applicants_id == 'None':
            new_applicants_id = student_id
        else:
            new_applicants_id = applicants_id + ', ' + student_id

        id_field = 'job_id'
        id_field_value = job_id
        updates = dict(applicants_id=new_applicants_id)
        db.update_record_by_id(table_name, id_field, id_field_value, updates)

    @staticmethod
    def get_all_job_posting():
        table_name = tbn.JOB_POSTING
        return_fields = ('job_id', 'company_name', 'job_description', 'ctc', 'applicable_branches',
                         'total_rounds_count', 'current_round', 'application_close_date', 'applicants_id')
        conditions = dict()
        job_postings = db.fetch_record_by_condition(table_name, return_fields, conditions)
        return job_postings

    @staticmethod
    def set_round_job_posting(job_id: str, new_applicants_id: tuple[str, ...], new_current_round: str):
        table_name = tbn.JOB_POSTING
        id_field = 'job_id'
        id_field_value = job_id

        new_applicants_id = ', '.join(new_applicants_id)
        updates = dict(applicants_id=new_applicants_id, current_round=new_current_round)

        db.update_record_by_id(table_name, id_field, id_field_value, updates)

    @staticmethod
    def set_students_job_status(company_name, students_id: tuple[str, ...]):
        table_name = tbn.STUDENT_ACCOUNT
        updates = dict(company_name=company_name, placement_status='placed')

        conditions = []
        for student_id in students_id:
            conditions.append(('student_id', student_id))

        conditions = tuple(conditions)
        db.update_record_by_condition(table_name, updates, conditions)

    @staticmethod
    def close_job_process(job_id):
        table_name = tbn.JOB_POSTING
        id_field = 'job_id'
        id_field_value = job_id

        db.delete_record_by_id(table_name, id_field, id_field_value)
