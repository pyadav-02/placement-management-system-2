import utility.table_names as tbn
from utility import utils as db


class AuthenticationFunctionality:
    @staticmethod
    def is_valid(account_id, password, role):
        table_name = tbn.CREDENTIALS
        return_fields = ('account_id',)
        conditions = dict(account_id=account_id, password=password, role=role)

        result = db.fetch_record_by_condition(table_name, return_fields, conditions)

        if result:
            return True
        return False
