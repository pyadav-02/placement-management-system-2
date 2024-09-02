import datetime
import bcrypt
import re
INVALID = 'Invalid input please enter valid input'


def get_choice(choices):
    choices = tuple(map(str, choices))
    choice = input('Enter input: ')

    while choice not in choices:
        print(INVALID)
        choice = input('Enter input: ')

    return int(choice)


def get_account_id(role):
    account_id = input('Enter account id: ')

    def is_valid(aid):
        if len(aid) == 10 and aid[0] == role[0] and aid[1:].isdigit():
            return True
        return False

    while not is_valid(account_id):
        print(INVALID)
        account_id = input('Enter account id: ')

    return account_id


def get_name(input_string):
    full_name = input(input_string).split()

    while not (all([name.isalpha() for name in full_name]) and len(full_name) > 0):
        print(INVALID)
        full_name = input(input_string).split()

    full_name = [name.lower() for name in full_name]
    full_name = [name.capitalize() for name in full_name]
    full_name = ' '.join(full_name)
    return full_name


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
        print(INVALID)
        number = input(input_string)
    return number


def get_cgpa(out_of=10):
    cgpa = get_float('Enter your cgpa: ')
    while not float(cgpa) <= out_of:
        print(INVALID)
        cgpa = get_float('Enter cgpa: ')
    return cgpa


def get_integer_input(input_string):
    choice = input(input_string)
    while not choice.isdigit():
        print(INVALID)
        choice = input(input_string)
    return choice


def get_year(initial=2011, max_course_time=4):
    current_date = datetime.datetime.now()
    current_year = current_date.year

    choice = get_integer_input('Enter year: ')
    while not initial + max_course_time - 1 <= int(choice) <= current_year + max_course_time - 1:
        print(INVALID)
        choice = get_integer_input('Enter year: ')

    return choice


def get_one_time_choice(all_choices: tuple, left_choices: list, input_string, warning_string=INVALID) -> int:
    choice = int(get_integer_input(input_string))
    while choice not in left_choices:
        if choice in all_choices:
            print(warning_string)
        else:
            print(INVALID)
        choice = int(get_integer_input(input_string))

    left_choices.remove(choice)

    return choice


def is_date_valid(date):
    date = date.split('-')
    if len(date) != 3:
        return False
    elif len(date[0]) != 2 or not date[0].isdigit():
        return False
    elif len(date[1]) != 2 or not date[1].isdigit():
        return False
    elif len(date[2]) != 4 or not date[2].isdigit():
        return False
    return True


def get_date(input_string):
    date = input(input_string)
    while not is_date_valid(date):
        print(INVALID)
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
    expression1 = r'(.+){8,}'
    expression2 = r'[a-zA-Z0-9]+'
    expression3 = r'[^a-zA-Z0-9]+'

    matches1 = re.findall(expression1, password)
    matches2 = re.findall(expression2, password)
    matches3 = re.findall(expression3, password)

    if matches1 and matches2 and matches3:
        return True
    return False


def get_password():
    password = input('Enter Password: ')
    while not is_password_strong(password):
        print('week password'
              '\npassword must be of at least 8 character'
              '\npassword must contains at least 1 upper letter'
              '\npassword must contains at least 1 lower letter'
              '\npassword must contains at least 1 special character')
        password = input('Enter Password: ')


def hash_password(password):
    string_byte = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(string_byte, bcrypt.gensalt())
    hashed_password = str(hashed_password)[2:-1]
    return hashed_password


def is_hash_password_valid(password, hashed_password):
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    result = bcrypt.checkpw(password=password, hashed_password=hashed_password)
    return result
