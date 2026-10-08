from model.product import Product


class ProductRepository:

    def __init__(self, db_connection):
        self.db = db_connection

    def save(self, product : Product):

        cursor = self.db.cursor()
        try:
            saved_product = cursor.execute("INSERT INTO products (id, name, price, quantity) Values (?,?,?,?)",
                            (product.id, product.name, product.price, product.quantity))
            self.db.commit()

            return saved_product.lastrowid

        except Exception as e:
            print("Houve um erro ao inserir os dados na base de dados: ", e)
            self.db.rollback()

        finally : 
            cursor.close()


    def get_by_id(self, product_id : str):

        cursor = self.db.cursor()

        try:
            return cursor.execute("Select * from products where id = ?",(product_id,)).fetchall()

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