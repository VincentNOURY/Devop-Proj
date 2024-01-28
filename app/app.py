import os
from mysql.connector import (connection)
from flask import Flask, request

app = Flask(__name__)

cnx = connection.MySQLConnection(user="root", password="root",
                                 host=os.environ["MYSQL_HOST"],
                                 database="employees")

cursor = cnx.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS employees (emp_no INT, first_name VARCHAR(255), last_name VARCHAR(255), hire_date DATE)")

cursor.close()
cnx.close()

@app.route("/")
def main():
  return "Welcome!<br><a href='/hay'>How are you?</a><br><a href='/lire'>Read</a><br><a href='/form'>Add</a><br>"

@app.route("/hay")
def hello():
  return "I am good, how about you?"


@app.route("/lire")
def read():
  cnx = connection.MySQLConnection(user="root", password="root",
                                 host=os.environ["MYSQL_HOST"],
                                 database="employees")

  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM employees")
  result = cursor.fetchall()
  cursor.close()
  cnx.close()
  return result

@app.route("/form")
def form():
    return """
      <form action="/afd" method="POST">
      <label for="emp_no">emp_no:</label><br>
      <input type="text" id="emp_no" name="emp_no"><br>
      <label for="first_name">first_name:</label><br>
      <input type="text" id="first_name" name="first_name"><br>
      <label for="last_name">last_name:</label><br>
      <input type="text" id="last_name" name="last_name"><br>
      <label for="hire_date">hire_date:</label><br>
      <input type="date" id="hire_date" name="hire_date"><br><br>
      <input type="submit" value="Submit">
    </form>
    """

@app.route("/afd", methods=["POST"])
def add():
  cnx = connection.MySQLConnection(user="root", password="root",
                                 host=os.environ["MYSQL_HOST"],
                                 database="employees")

  cursor = cnx.cursor()
  emp_no = request.form["emp_no"]
  first_name = request.form["first_name"]
  last_name = request.form["last_name"]
  hire_date = request.form["hire_date"]
  cursor.execute("INSERT INTO employees (emp_no, first_name, last_name, hire_date) VALUES (%s, %s, %s, %s)", (emp_no, first_name, last_name, hire_date))
  cnx.commit()
  cursor.close()
  cnx.close()
  return "Employee added<br><a href='/lire'>Read</a><br>"


@app.route("/lireid/<id>")
def read_by_id(id):
  cnx = connection.MySQLConnection(user="root", password="root",
                                 host=os.environ["MYSQL_HOST"],
                                 database="employees")

  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM employees WHERE emp_no = %s", (id,))
  row = cursor.fetchone()
  cursor.close()
  cnx.close()
  if row is None:
    return "Not found"
  else:
    return row[0]
    
@app.route("/sup/<id>")
def delete(id):
  cnx = connection.MySQLConnection(user="root", password="root",
                                 host=os.environ["MYSQL_HOST"],
                                 database="employees")

  cursor = cnx.cursor()
  cursor.execute("DELETE FROM employees WHERE emp_no = %s", (id,))
  cnx.commit()  
  cursor.close()
  cnx.close()
  return "Employee deleted"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")