import utility.table_names as tbn
from utility import utils as db
from utility.validation_utils import is_hash_password_valid


class Authentication:
    @staticmethod
    def is_credential_valid(account_id, password, role):
        table_name = tbn.CREDENTIALS
        return_fields = ('password',)
        conditions = dict(account_id=account_id, role=role)

        result = db.fetch_record_by_condition(table_name, return_fields, conditions)

        if len(result) == 0:
            return False
        return is_hash_password_valid(password, result[0][0])
