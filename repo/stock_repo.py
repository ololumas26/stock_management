from model.stock import Stock


class StockRepository:

    def __init__(self, db_connection):
        self.db = db_connection


    def get_by_product_id(self, product_id : str):

        cursor = self.db.cursor()
        try:
            return cursor.execute("SELECT * FROM stocks where product_id = ?", (product_id,)).fetchone()
        except Exception as e:
            print("Houve um erro ao obter o stock do produto")

        finally:
            cursor.close()

    def regist_new_stock(self, stock : Stock):

        cursor = self.db.cursor()
    
        try:

            last_row = cursor.execute(
                "UPDATE stocks SET quantity = ? where product_id = ?",
                (stock.quantity, stock.product_id),
            ).lastrowid
            self.db.commit()
            return last_row
        
        except Exception as e:
            print("Something goes wrong while inserting data in database: ", e)

        finally:
            cursor.close()


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