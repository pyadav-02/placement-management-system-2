import datetime
import calendar
import bcrypt
import re
INVALID_LOCK = 'Invalid input please enter valid input'
BACK = """
press 1 to continue giving input
press 2 to go back
"""


def get_choice(choices):
    choices = tuple(map(str, choices))
    choice = input('Enter input: ')

    while choice not in choices:
        print(INVALID_LOCK)
        choice = input('Enter input: ')

    return int(choice)


def get_account_id():
    account_id = input('Enter account id: ')
    go_back = 1
    while not account_id.isalnum():
        print("---invalid id formate---")
        print(BACK)
        go_back = get_choice((1, 2))
        if go_back == 2:
            break
        account_id = input('Enter account id: ')

    return account_id, go_back == 2


def create_account_id(role):
    def is_account_id_valid(aid):
        if aid[0] == role[0] and len(aid[1:]) == 9 and aid[1:].isdigit():
            return True
        return False

    go_back = 1
    account_id = input('Enter account id: ')
    while not is_account_id_valid(account_id):
        print(INVALID_LOCK)
        print(BACK)
        go_back = get_choice((1, 2))
        if go_back == 2:
            break
        account_id = input('Enter account id: ')

    return account_id, go_back == 2


def get_name(input_string):
    full_name = input(input_string).split()
    go_back = 1
    while not (all([name.isalpha() for name in full_name]) and len(full_name) > 0):
        print(INVALID_LOCK)
        print(BACK)
        go_back = get_choice((1, 2))
        if go_back == 2:
            break
        full_name = input(input_string).split()

    full_name = [name.lower() for name in full_name]
    full_name = [name.capitalize() for name in full_name]
    full_name = ' '.join(full_name)
    return full_name, go_back == 2


def get_branch():
    branches = ('cse', 'it', 'ee', 'me', 'ce')
    for i in range(len(branches)):
        print(f'press {i+1} to chose {branches[i]}')

    choice = get_choice([1, 2, 3, 4, 5])
    return branches[choice-1]


def is_float(number):
    number = number.split('.')
    if len(number) == 1:
        return number[0].isdigit()
    elif len(number) == 2:
        return number[0].isdigit() and number[1].isdigit()
    return False


def get_float(input_string):
    number = input(input_string)
    while not is_float(number):
        print(INVALID_LOCK)
        number = input(input_string)
    return number


def get_cgpa(out_of=10):
    cgpa = get_float('Enter your cgpa: ')
    go_back = 1
    while not float(cgpa) <= out_of:
        print(INVALID_LOCK)
        print(BACK)
        go_back = get_choice((1, 2))
        if go_back == 2:
            break
        cgpa = get_float('Enter cgpa: ')
    return cgpa, go_back == 2


def get_integer_input(input_string):
    choice = input(input_string)
    while not choice.isdigit():
        print('invalid input: Enter only integer')
        choice = input(input_string)
    return choice


def get_year(initial=2011, max_course_time=4):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    choice = get_integer_input('Enter year: ')
    go_back = 1
    while not initial + max_course_time - 1 <= int(choice) <= current_year + max_course_time - 1:
        print(INVALID_LOCK)
        print(BACK)
        go_back = get_choice((1, 2))
        if go_back == 2:
            break
        choice = get_integer_input('Enter year: ')

    return choice, go_back == 2


def get_one_time_choice(all_choices: tuple, left_choices: list, input_string, warning_string=INVALID_LOCK) -> int:
    choice = int(get_integer_input(input_string))
    while choice not in left_choices:
        if choice in all_choices:
            print(warning_string)
        else:
            print(INVALID_LOCK)
        choice = int(get_integer_input(input_string))

    if choice in left_choices:
        left_choices.remove(choice)

    return choice


def is_date_valid(date, future=False):
    date = date.split('-')
    if len(date) != 3:
        return False
    elif len(date[0]) != 2 or not date[0].isdigit():
        return False
    elif len(date[1]) != 2 or not date[1].isdigit():
        return False
    elif len(date[2]) != 4 or not date[2].isdigit():
        return False

    day, month, year = map(int, date)
    if (year < 1) or (1 > month or month > 12) or (1 > day or day > calendar.monthrange(year, month)[1]):
        return False

    if future and datetime.date(year, month, day) < datetime.date.today():
        return False

    return True


def get_date(input_string):
    date = input(input_string)
    while not is_date_valid(date, future=True):
        print(INVALID_LOCK)
        date = input(input_string)
    return date


def get_selected_applicants(applicants_id: tuple, not_last_round=True):
    selected_applicants_id = []
    round_string = 'for next round'

    for applicant_id in applicants_id:
        print(f"""
        -- make decision for student with student id: {applicant_id} --
        press 1 if student is selected {round_string * not_last_round}
        press 2 if student is not selected {round_string * not_last_round}
        """)
        choices = (1, 2)
        choice = get_choice(choices)

        if choice == 1:
            selected_applicants_id.append(applicant_id)

    return tuple(selected_applicants_id)


def is_password_strong(password):
    expression = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$'
    matches = re.findall(expression, password)
    if matches:
        return True
    return False


def get_password():
    password = input('Enter Password: ')
    go_back = 1
    while not is_password_strong(password):
        print('---week password---'
              '\npassword must be of at least 8 character'
              '\npassword must contains at least 1 upper letter'
              '\npassword must contains at least 1 lower letter'
              '\npassword must contains at least 1 special character')
        print(BACK)
        go_back = get_choice((1, 2))
        if go_back == 2:
            break
        password = input('Enter Password: ')

    return password, go_back == 2


def get_hashed_password(password):
    string_byte = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(string_byte, bcrypt.gensalt())
    hashed_password = str(hashed_password)[2:-1]
    return hashed_password


def is_hash_password_valid(password, hashed_password):
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    result = bcrypt.checkpw(password=password, hashed_password=hashed_password)
    return result
