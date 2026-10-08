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