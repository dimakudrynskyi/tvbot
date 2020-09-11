import sqlite3

class Sqlighter:

    def __init__(self, database):
        """Connect to db"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_remind(self, user_id, caption):
        """Add remind to db"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'remind' (`user_id`, `remind`) VALUES(?,?)", (user_id,caption))
    
    def delete_remind(self, user_id, caption):
        """Delete remind from db""" 
        with self.connection:
            data = self.cursor.execute("SELECT remind FROM remind WHERE user_id=?", (user_id,)).fetchall()
            for row in data:
                new_row =  ''.join(row)
                if new_row == caption:
                    return self.cursor.execute("DELETE FROM 'remind' WHERE user_id=? AND remind=?", (user_id, new_row,))

    def delete_all_remind(self, user_id):
        """Add remind to db"""
        with self.connection:
            return self.cursor.execute("DELETE FROM 'remind' WHERE user_id=?", (user_id,)) 

    def send_remind(self, user_id):
        """Delete remind from db""" 
        with self.connection:
            data = self.cursor.execute("SELECT remind FROM remind WHERE user_id=?", (user_id,)).fetchall()
            for row in data:
                new_row =  ''.join(row)
            return new_row

    def close(self):
        """Close connect with db""" 
        self.connection.close()