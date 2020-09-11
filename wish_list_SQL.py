import sqlite3

class sqlighter:

    def __init__(self, database):
        """Connect to db"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_to_wish_list(self, user_id, caption):
        """Add film\series to db"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'wish_list' (`user_id`, `wish_list`) VALUES(?,?)", (user_id,caption))

    def remove_wish_list(self, user_id, caption):
        """Check if there is already a user in the database"""
        with self.connection:
            data = self.cursor.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,)).fetchall()
            for row in data:
                new_row =  ''.join(row)
                if new_row == caption:
                   return self.cursor.execute(f"DELETE FROM wish_list WHERE wish_list=? AND user_id={user_id}", (row))            

    def select_wish_list(self, user_id):
        """Select wish list from db"""
        with self.connection:
            data = self.cursor.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,)).fetchall()
            for row in data:
                new_row =  ''.join(row)
            return new_row



    def close(self):
        """Close connect with db""" 
        self.connection.close()
    