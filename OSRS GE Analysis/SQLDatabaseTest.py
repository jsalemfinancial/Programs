import mysql.connector

class Manage():
  def __init__(self, host, user, password):
    try:
      self.db = mysql.connector.connect(host = host, user = user, password = password)
    except:
      print("Connection error. Is server running?")

    print("Connected!")
    self.cursor = self.db.cursor()

  def showDatabases(self):
      self.cursor.execute("SHOW DATABASES")

      for db in self.cursor:
        print(db)

  def input(self, string):
    try:
      self.cursor.execute(string)
    except:
      print("Something went wrong!\n")