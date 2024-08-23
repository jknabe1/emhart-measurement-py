from flask import Flask, render_template
import pymysql
import pymysql.cursors

app = Flask(__name__)

LOCALHOST = "127.0.0.1"
USER = "root"
DATABASE = "emhart"

def connect():
    connection = None
    try:
        connection = pymysql.connect(host=LOCALHOST, user=USER, password="", database=DATABASE, cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print(f"Error when connecting to database: {e}")
    
    return connection

def disconnect(connection):
    try:
        connection.close()
    except Exception as e:
        print(f"Error when disconnecting from database: {e}")

@app.route('/users')
def users():
    connection = connect()
    users = []
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `login`"
            cursor.execute(sql)
            users = cursor.fetchall()
    finally:
        disconnect(connection)
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)