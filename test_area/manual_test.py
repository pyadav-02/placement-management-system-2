import re

password = 'abcd$A0dsfdf'

expression1 = r'[^.]{8,}'
expression2 = r'[a-zA-Z0-9]+'
expression3 = r'[^a-zA-Z0-9]+'

matches1 = re.findall(expression1, password)
matches2 = re.findall(expression2, password)
matches3 = re.findall(expression3, password)

print(matches3)
