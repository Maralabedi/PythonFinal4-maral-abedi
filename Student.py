from config.database import get_connection

class Student:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                math REAL DEFAULT 0,
                english REAL DEFAULT 0,
                programming REAL DEFAULT 0,
                religion REAL DEFAULT 0,
                arabic REAL DEFAULT 0,
                physics REAL DEFAULT 0,
                chemistry REAL DEFAULT 0,
                biology REAL DEFAULT 0
            )
        ''')
        self.conn.commit()

    def all(self):
        self.cursor.execute("SELECT * FROM students ORDER BY last_name, first_name")
        return self.cursor.fetchall()

    def find(self, sid):
        self.cursor.execute("SELECT * FROM students WHERE id=?", (sid,))
        return self.cursor.fetchone()

    def create(self, data):
        sql = '''INSERT INTO students (first_name,last_name,age,math,english,programming,religion,arabic,physics,chemistry,biology)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
        self.cursor.execute(sql, data)
        self.conn.commit()

    def update(self, sid, data):
        sql = '''UPDATE students SET first_name=?,last_name=?,age=?,math=?,english=?,programming=?,religion=?,arabic=?,physics=?,chemistry=?,biology=?
                 WHERE id=?'''
        self.cursor.execute(sql, (*data, sid))
        self.conn.commit()

    def delete(self, sid):
        self.cursor.execute("DELETE FROM students WHERE id=?", (sid,))
        self.conn.commit()

    def search(self, keyword):
        self.cursor.execute("SELECT * FROM students WHERE first_name LIKE ? OR last_name LIKE ?", 
                           (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()