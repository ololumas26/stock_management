from decimal import Decimal
from uuid import uuid4
from database import cnn, create_table


class Product:

    def __init__(self):

        self.id = ""
        self.name = ""
        self.quantity = 0
        self.price = ""
  
    @classmethod
    def regist_product(cls, name : int, price : Decimal , quantity : int = 0):

        if not name:
            raise ValueError("O nome do produto é obrigatório")
        
        if price < 0 or quantity < 0:
            raise ValueError("Preço ou quantidde não podem ser menores que zero")
        
        cls.id = str(uuid4())
        cls.name = name
        cls.quantity = quantity
        cls.price = price

        cls.save(cls)

    def save(self):
        
        cursor = cnn.cursor()
        try:
            cursor.execute("INSERT INTO products (id, name, price, quantity) Values (?,?,?,?)",
                           (self.id, self.name, self.price, self.quantity))
            cnn.commit()
            print("Produto criado com sucesso")

        except Exception as e:
            print("Houve um erro ao inserir os dados na base de dados: ", e)

        finally : 
            cnn.close()

    def get_products(self):

        cursor = cnn.cursor()
        try:

            return cursor.execute("select * from products").fetchall()

        except Exception:
            print("Houve um erro na comunicação com a base de dados.")

        finally : 
            cursor.close()

    def get_by_name(self, name : str):

        cursor = cnn.cursor()
        try:

            return cursor.execute("select * from products where name LIKE ?;",(f"%{name}%",)).fetchall()

        except Exception as e:
            print("Houve um erro na comunicação com a base de dados: ", e)

        finally : 
            cursor.close()


create_table()