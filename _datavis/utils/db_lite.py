import sqlite3

conn = sqlite3.connect(':memory:')
curs = conn.cursor()

curs.execute("""CREATE TABLE employees (
            first text,
            last text,
            pay integer
            )""")


def insert_emp(emp):
    with conn:
        curs.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {
            'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(lastname):
    curs.execute("SELECT * FROM employees WHERE last=:last",
                 {'last': lastname})
    return curs.fetchall()


def update_pay(emp, pay):
    with conn:
        curs.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                     {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        curs.execute("DELETE from employees WHERE first = :first AND last = :last",
                     {'first': emp.first, 'last': emp.last})
