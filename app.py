from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
        cnx = mysql.connector.connect(user='root', password='root',
                                                                    host=os.environ['MYSQL_HOST'],
                                                                    database='users')
        cursor = cnx.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), email VARCHAR(255))")
        
        for i in range(20):
                add_user = ("INSERT INTO users "
                                "(username, email) "
                                "VALUES (%s, %s)")
                data_user = ('user' + str(i), 'user' + str(i) + '@example.com')
                cursor.execute(add_user, data_user)       
        
        cnx.commit()

        query = ("SELECT username, email FROM users")
        cursor.execute(query)
        for (username, email) in cursor:
                print("{} has email {}".format(username, email))

        cursor.close()
        cnx.close()

        return 'Hello, World!'

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')