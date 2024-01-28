import os
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

mysql_database_host = 'MYSQL_HOST' in os.environ and os.environ['MYSQL_HOST'] or 'localhost'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'employee_db'
app.config['MYSQL_DATABASE_HOST'] = mysql_database_host
app.config['MYSQL_DATABASE_PORT'] = os.environ['MYSQL_PORT'] if 'MYSQL_PORT' in os.environ else 3306
mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS employees (emp_no INT, first_name VARCHAR(255), last_name VARCHAR(255), hire_date DATE)")
cursor.execute("CREATE DATABASE IF NOT EXISTS employee_db")
cursor.execute("USE employee_db")

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