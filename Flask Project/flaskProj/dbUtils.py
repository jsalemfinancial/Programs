import mysql.connector


class DBErrors(Exception):
    pass

class DBCommands():
    def __init__(self, dbConfig: dict) -> None:
        self.config = dbConfig

    def __enter__(self) -> "cursor":
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as error:
            raise Exception(error)

    def __exit__(self, executeType, executeValue, executeTrace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()