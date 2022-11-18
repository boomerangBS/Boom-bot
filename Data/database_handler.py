import os
import datetime
import sqlite3
class DatabaseHandler():
  def __init__(self,database_name : str):
    self.con=sqlite3.connect("Data/database.db")
    self.con.row_factory = sqlite3.Row

  def add_tempmute(self,user_id : int,guild_id : int,expiration_time : datetime.datetime):
    cursor = self.con.cursor()
    query = "INSERT INTO tempmute (user_id,guild_id,expiration_time) VALUES (?,?,?);"
    cursor.execute(query,(user_id,guild_id,expiration_time))
    cursor.close()
    self.con.commit()

  def active_tempmute_to_revoke(self, guild_id : int) -> [dict]:
		 cursor = self.con.cursor()
		 query = "SELECT * FROM Tempmute WHERE guild_id = ? AND active = 1 AND expiration_date < ?;"
		 cursor.execute(query, (guild_id, datetime.datetime.utcnow()))
		 result = list(map(dict,   cursor.fetchall()))
		 cursor.close()
		 return result

  def revoke_tempmute(self, tempmute_id : int):
		 cursor = self.con.cursor()
		 query = "UPDATE Tempmute SET active = 0 WHERE id = ?;"
		 cursor.execute(query, (tempmute_id,))
		 cursor.close()
		 self.con.commit()
    