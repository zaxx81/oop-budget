import functools, csv, os
from classes.expenses import Expenses

class Budget:
  def __init__(self, name) -> None:
    self.name = name
    self.income_monthly = 0.0
    self.expenses_monthly = 0.0
    self.transactions = Expenses.objects()
    self.totals_by_cat = {}
 

  def __str__(self) -> str:
    return f'Budge: {self.name}'

  def update_income(self):
    print('Adding a new expense.')
    income = float(input('Enter a new monthly income: '))
    self.income_monthly = income
  
  def add_expense(self):
    print('Adding a new expense.')
    descr = input('Enter a description: ')
    cat = input('Enter a category: ')
    amount = float(input('Enter an amount: '))
    self.transactions.append(Expenses(description=descr, category=cat, amount=amount))

  def remove_expense(self):
    print('Removing an expense.')
    for item in self.transactions:
      print(item)
    removal_id = input('Enter the ID of the expense to remove: ')
    
    if removal_id:
      for item in self.transactions:
        if item.id == int(removal_id):
          self.transactions.remove(item)

  def calc_expenses(self):
    category_keys = Expenses.expense_by_categories.keys()

    for key in category_keys:
      self.totals_by_cat.update({key: 0.0})

    for key in category_keys:
      category_list = Expenses.expense_by_categories.get(key)

      if len(category_list) == 1:
        subtotal = category_list[0].amount
      else:
        subtotal = functools.reduce(lambda a, b: a.amount + b.amount, category_list)
      self.totals_by_cat[key] = subtotal
      self.expenses_monthly = self.expenses_monthly + subtotal

  def show_budget(self):
    
    self.calc_expenses()
    
    if self.income_monthly == 0:
      print('Warning! You forgot to set your monthly income.')
      self.update_income()
    
    print(f'\n---{self.name}---')
    print('Monthly Income ${:,.2f}'.format(self.income_monthly))
    print('Monthly Expenses ${:,.2f}\n'.format(self.expenses_monthly))

    print(f'--Categories--')
    
    for categories in self.totals_by_cat:
      cat_amount = self.totals_by_cat.get(categories)
      cat_percentage = cat_amount / self.income_monthly * 100
      cat_amount_str = '${:,.2f}'.format(cat_amount)
      cat_percentage_str = '{:.1f}%'.format(cat_percentage)
      print(f'{categories}: {cat_amount_str} ({cat_percentage_str})')
    
    input('Press any key to go back to the main menu')

  def save_exit(self):
    choice = input('Exiting...would you like to save expenses? [y/n]')
    if (choice.lower() == 'y') or (choice.lower() == 'yes'):
      print('Saving...')
      my_path = os.path.abspath(os.path.dirname(__file__))
      my_file = '../data/expenses.csv'
      path = os.path.join(my_path, my_file)
      
      with open(path, 'w', newline='') as csvfile:
        data = csv.writer(csvfile)
        data.writerow(['description', 'category', 'amount'])

        for expense in self.transactions:
          row = [expense.description, expense.category, expense.amount]
          data.writerow(row)

      print('Exiting...')
      return True

    elif (choice.lower() == 'n') or (choice.lower() == 'no'):
        return True
    else:
      return False
