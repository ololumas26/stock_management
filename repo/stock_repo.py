from model.stock import Stock


class StockRepository:

    def __init__(self, db_connection):
        self.db = db_connection


    def save(self, stock : Stock):
        cursor = self.db.cursor()

        try:

            last_row = cursor.execute(
                "INSERT INTO stock (id, product_id, quantity) VALUES (?, ?, ?)",
                (stock.id, stock.product_id, stock.quantity),
            ).lastrowid
            self.db.commit()
            return last_row
        
        except Exception as e:
            print("Something goes wrong while inserting data in database: ", e)

        finally:
            cursor.close()