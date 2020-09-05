import sqlite3

# class SQLighter:

#     def __init__(self, database):
#         """Connect to db"""
#         self.connection = sqlite3.connect(database)
#         self.cursor = self.connection.cursor()

#     # def add_user(self, user_id)


#     # def get_subscriptions(self, status = True):
#     #     """We get all active subscribers of the bot"""
#     #     with self.connection:
#     #         return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

#     # def subscriber_exists(self, user_id):
#     #     """Check if there is already a user in the database"""
#     #     with self.connection:
#     #         result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
#     #         return bool(len(result))

#     # def add_subscriber(self, user_id, status = True):
#     #     """Add new user"""
#     #     with self.connection:
#     #         return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

#     # def update_subscription(self, user_id, status):
#     #     """Update subscribe ststus for user """
#     #     with self.connection:
#     #         return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))


#     def close(self):
#         """Close connect with db"""
#         self.connection.close()

