from functools import total_ordering
from classes.budget import Budget
from classes.expenses import Expenses
from menu import menu

my_budget = Budget("Budget June 2022")
menu(my_budget)