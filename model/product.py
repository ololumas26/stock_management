from decimal import Decimal
from uuid import uuid4
from database import cnn, create_table


class Product:

    def __init__(self, name : str, price : Decimal, quantity : int = 0):

        # Falha antes de criar o objeto

        if not name:
            raise ValueError("O nome do produto é obrigatório")
        
        if price < 0 or quantity < 0:
            raise ValueError("Preço ou quantidde não podem ser menores que zero")

        self.id = str(uuid4())
        self.name = name
        self.price = price
        self.quantity = quantity

  
    