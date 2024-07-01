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

def ins():
    connection = get_db_connection()
    if connection is None:
        print("Content-type: text/html\n")
        print("Database connection failed")
        return
    
    form = cgi.FieldStorage()
    a = form.getvalue('e1')
    b = form.getvalue('p1')

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO user (email, password) VALUES (%s, %s)"
        cursor.execute(sql, (a, b))
        connection.commit()  # Commit the transaction

        c = http.cookies.SimpleCookie()
        c['mou'] = a
        c['mou']['expires'] = 24*60*60
        print(c)
        print("Content-type: text/html\n")
        print('''<html>
            <head><title>Insertion Success</title></head>
            <body><h2>User Created Successfully</h2></body>
        </html>''')

    except mysql.connector.Error as e:
        print("Content-type: text/html\n")
        print(f"Error executing query: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    ins()


