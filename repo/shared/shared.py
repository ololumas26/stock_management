

class Shared:

    def __init__(self, db_connection):
        self.db = db_connection


    def get_totals(self, table_name : str):

        cursor = self.db.cursor()
        try:

            return cursor.execute(f"SELECT COUNT(id) from {table_name}").fetchone()[0]

        except Exception as e:
            print(f"An error occurs while retrivieng total from table {table_name}: ", e)
