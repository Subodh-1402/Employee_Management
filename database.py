from flask import g

import sqlite3

def connect_to_databse():
  con = sqlite3.connect('employee_manage.db')

  con.row_factory = sqlite3.Row
  return con

def get_database():
    if not hasattr(g, 'employee_manage.db'):
        g.employee_manage_db = connect_to_databse()

    return g.employee_manage_db


