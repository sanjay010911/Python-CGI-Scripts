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

def delete_user():
    connection = get_db_connection()
    if connection is None:
        print("Content-type: text/html\n")
        print("Database connection failed")
        return
    
    form = cgi.FieldStorage()
    user_id = form.getvalue('i1')

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM user WHERE id=%s"
        cursor.execute(sql, (user_id,))
        connection.commit()  # Commit the transaction

        print("Content-type: text/html\n")
        print('''<html>
            <head><title>Delete Success</title></head>
            <body><h2>User Deleted Successfully</h2></body>
        </html>''')

    except mysql.connector.Error as e:
        print("Content-type: text/html\n")
        print(f"Error executing query: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    delete_user()
