from model.stock import Stock
from model.moviment import MovimentsType, Movements

class StockRepository:

    def __init__(self, db_connection):
        self.db = db_connection


    def get_by_product_id(self, product_id : str):

        cursor = self.db.cursor()
        try:
            return cursor.execute("SELECT * FROM stocks where product_id = ?", (product_id,)).fetchone()
        except Exception as e:
            print("Houve um erro ao obter o stock do produto")
            raise

        finally:
            cursor.close()

    def regist_new_stock(self, product_id, quantity, movement : Movements):

        cursor = self.db.cursor()
        mov_sign = '+' if movement.mov_type == MovimentsType.ENTRANCE.value else '-'

        try:
            cursor.execute('BEGIN IMMEDIATE')

            current = self.get_by_product_id(product_id)

            if not current:
                raise RuntimeError("Product not found")

            current_quantity = current[len(current) - 1]

            if current_quantity is None:
                raise RuntimeError("Product without stock registered")

            if movement.mov_type == MovimentsType.EXIT.value:
                if current_quantity < quantity:
                    raise ValueError("Not enough stock")
                
            cursor.execute(
                f"""UPDATE stocks
                   SET quantity = quantity {mov_sign} ? where product_id = ?""",
                (quantity, product_id),
            ).lastrowid

            
            cursor.execute("INSERT INTO movements(id, product_id, mov_type, quantity_moved, note) VALUES(?,?,?,?,?)",
                           (movement.id, movement.product_id, movement.mov_type,movement.quantity ,movement.note))
            cursor.execute("COMMIT")
            return True
        
        except Exception as e:
            print("Something goes wrong while inserting data in database: ", e)
            cursor.execute("ROLLBACK")
            raise

        finally:
            cursor.close()


    def get_stock_less_than_5(self):

        cursor = self.db.cursor()
        try:
        
            return cursor.execute("""
                    select p.name, s.quantity from products p
                    JOIN stocks s on p.id = s.product_id
                    where s.quantity < 5
                """).fetchall()
    
        except Exception as e:
            print("Something goes wrong while performing the query: ", e)
            raise

        finally:
            cursor.close()

    def get_stock_total_value(self):

        cursor = self.db.cursor()
        try:
        
            return cursor.execute("""
                    select SUM(p.price * s.quantity) as total_stock_value from products p
                    join stocks s on p.id = s.product_id
                """).fetchone()
    
        except Exception as e:
            print("Something goes wrong while performing the query: ", e)
            raise

        finally:
            cursor.close()
        


    def save(self, stock : Stock):

        cursor = self.db.cursor()

        try:

            last_row = cursor.execute(
                "INSERT INTO stocks (id, product_id, quantity) VALUES (?, ?, ?)",
                (stock.id, stock.product_id, stock.quantity),
            ).lastrowid
            self.db.commit()
            return last_row
        
        except Exception as e:
            print("Something goes wrong while inserting data in database: ", e)
            raise

        finally:
            cursor.close()