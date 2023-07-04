import mysql.connector
class DataBase:
    def __init__(self) -> None:
            self.connection=mysql.connector.connect(
                  host="localhost",
                  user="root",
                  password="",
                  database="game"
            )
            self.cursor=self.connection.cursor()