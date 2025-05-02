from datetime import datetime

date_format = '%d-%m-%Y'
CATEGORIES = {"I": 'Income', "E": 'Expense'}
def get_date(prompt, allow_default=False):
  date_st = input(prompt)
  if allow_default and not date_st:
    return datetime.now().strftime(date_format)
  try:
    date = datetime.strptime(date_st, date_format)
    return date.strftime(date_format)
  except ValueError:
    print('Invalid date format. Please use dd-mm-yyyy.')
    return get_date(prompt, allow_default)

def get_amount():
  try:
    amount = float(input('Enter amount: '))
    if amount <= 0:
      raise ValueError
    return amount
  except ValueError as e:
    print('Invalid amount. Please enter a positive number.', e)
    return get_amount()

def get_description():
  description = input('Enter description: ')
  if not description:
    print('Description cannot be empty.')
    return get_description()
  return description

def get_category():
  category = input('Enter category I for income or E for expense: ').upper()
  if category not in CATEGORIES:
    print('Invalid category. Please enter "I" for income or "E" for expense.')
    return get_category()
  return 'Income' if category == 'I' else 'Expense'