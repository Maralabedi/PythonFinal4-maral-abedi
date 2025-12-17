# config/database.py
import sqlite3

def get_connection():
    conn = sqlite3.connect('students_grades.db')
    conn.row_factory = sqlite3.Row
    return conn