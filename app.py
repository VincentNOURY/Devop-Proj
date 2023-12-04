from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def hello_world():
        cnx = mysql.connector.connect(user='root', password='root',
                                                                    host='mysql',
                                                                    database='users')
        cursor = cnx.cursor()
        query = ("SELECT username, email FROM users")
        cursor.execute(query)

        for (username, email) in cursor:
            print("{}: {}".format(username, email))

        cursor.close()
        cnx.close()

        return 'Hello, World!'

if __name__ == '__main__':
        app.run(debug=True, port=80)