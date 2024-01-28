import os
from mysql.connector import (connection)
from flask import Flask, request

app = Flask(__name__)

cnx = connection.MySQLConnection(user='root', password='root',
                                 host=os.environ['MYSQL_HOST'],
                                 database='employees')

cursor = cnx.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS employees (emp_no INT, first_name VARCHAR(255), last_name VARCHAR(255), hire_date DATE)")
cursor.close()
cnx.close()

@app.route("/")
def main():
  return "Welcome!"

@app.route('/hay')
def hello():
  return 'I am good, how about you?'


@app.route('/lire')
def read():
    cursor.execute("SELECT * FROM employees")
    row = cursor.fetchone()
    result = []
    while row is not None:
      result.append(row[0])
      row = cursor.fetchone()
    return ",".join(result)

@app.route('/form')
def form():
    return """
      <form action="/afd" method="POST">
      <label for="id">id:</label><br>
      <input type="text" id="id" name="id"><br>
      <label for="first_name">first_name:</label><br>
      <input type="text" id="first_name" name="first_name"><br>
      <label for="last_name">last_name:</label><br>
      <input type="text" id="last_name" name="last_name"><br>
      <label for="hire_date">hire_date:</label><br>
      <input type="text" id="hire_date" name="hire_date"><br><br>
      <input type="submit" value="Submit">
    </form>
    """

@app.route('/afd', methods=['POST'])
def add():
    id = request.form['id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    hire_date = request.form['hire_date']
    cursor.execute("INSERT INTO employees (emp_no, first_name, last_name, hire_date) VALUES (%s, %s, %s, %s)", (id, first_name, last_name, hire_date))
    conn.commit()
    return "Employee added"


@app.route('/lireid/<id>')
def read_by_id(id):
    cursor.execute("SELECT * FROM employees WHERE emp_no = %s", (id,))
    row = cursor.fetchone()
    if row is None:
      return "Not found"
    else:
      return row[0]

if __name__ == "__main__":
    app.run()