from model.product import Product
from model.stock import Stock
from model.moviment import Movements
from .shared.shared import Shared


class ProductRepository:

    def __init__(self, db_connection):
        self.db = db_connection
        self.shared = Shared(db_connection)

    def save(self, product : Product, stock : Stock, movement : Movements):

        cursor = self.db.cursor()
        try:

            cursor.execute('BEGIN IMMEDIATE')

            cursor.execute("INSERT INTO products (id, unique_ref , name, price) Values (?,?,?,?)",
                            (product.id, product.unique_ref ,product.name, product.price))

            last_product_saved_id = cursor.lastrowid
     
            cursor.execute("INSERT INTO stocks (id, product_id, quantity) Values (?,?,?)",
                            (stock.id, product.id, stock.quantity))

            cursor.execute(
                """
                INSERT INTO movements
                    (id, product_id, mov_type, quantity_moved, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    movement.id,
                    product.id,
                    movement.mov_type,
                    movement.quantity,
                    movement.note,
                ),
            )
            
            cursor.execute("COMMIT")
            return last_product_saved_id

        except Exception as e:
            print("Houve um erro ao inserir os dados na base de dados: ", e)
            cursor.execute('ROLLBACK')

        finally : 
            cursor.close()


    def get_by_id(self, product_id : str):

        cursor = self.db.cursor()

        try:
            return cursor.execute("Select * from products where id = ?",(product_id,)).fetchone() is not None

        except Exception as e:
            print("There's a mistake retrieing data from database ", e)
        
        finally : 
            cursor.close()


    def get_all(self, offset : int = 0, limit = 10):

        cursor = self.db.cursor()

        try:
            return cursor.execute("Select * from products limit ? offset ?", (limit, offset)).fetchall()

        except Exception as e:
            print("There's a mistake retrieing data from database ", e)
        
        finally : 
            cursor.close()

    def get_by_name(self, product_name : str):

        cursor = self.db.cursor()
        
        try:
            return cursor.execute("Select * from products where name LIKE ?", (f'%{product_name}%',)).fetchall()

        except Exception as e:
            print("There's a mistake retrieing data from database ", e)
        
        finally : 
            cursor.close()

    def get_total_products(self):
        return self.shared.get_totals('products')

  
