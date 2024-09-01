from flask import current_app
import MySQLdb.cursors
from mysql.connector import Error
from app import mysql


def execute_query(query, args=(), fetch_one=False, commit=False):
    
    cr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cr.execute(query, args)
    try:
        if commit:
            mysql.connection.commit()
            result = None
        elif fetch_one:
            result = cr.fetchone()
        else:
            result = cr.fetchall()
    except Error as e:
        print(f"Programming error: {e}")
        result = None
    finally:
        cr.close()
    return result


def insert_user(username, email, password):
    query = 'INSERT INTO login (user, email, password) VALUES (%s, %s, %s)'
    try:
        execute_query(query, (username, email, password), commit=True)
        return True
    except MySQLdb.IntegrityError:
        return False
