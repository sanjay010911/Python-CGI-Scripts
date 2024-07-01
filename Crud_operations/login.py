#!C:\Users\admin\AppData\Local\Programs\Python\Python310\python.exe
import mysql.connector
import cgi
import cgitb
import http.cookies

cgitb.enable()  # Enable detailed error reporting

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='student',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

def login():
    form = cgi.FieldStorage()
    a = form.getvalue('e1')
    b = form.getvalue('p1')
    
    connection = get_db_connection()
    if connection is None:
        print("Content-type: text/html\n")
        print("Database connection failed")
        return

    try:
        cursor = connection.cursor()
        sql = "SELECT id, email, password FROM user WHERE email=%s AND password=%s"
        cursor.execute(sql, (a, b))
        result = cursor.fetchone()

        if result:
            c = http.cookies.SimpleCookie()
            c['mou'] = a
            c['mou']['expires'] = 24*60*60
            print(c)
            print("Content-type: text/html\n")
            print('''<html>
                <head><title>Login Success</title></head>
                <body><h2>Successfully logged in</h2></body>
            </html>''')
        else:
            print("Content-type: text/html\n")
            print('''<html>
                <head><title>Login Failed</title></head>
                <body><h2>Failed to login</h2></body>
            </html>''')

    except mysql.connector.Error as e:
        print("Content-type: text/html\n")
        print(f"Error executing query: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    login()
