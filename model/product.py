from decimal import Decimal
from uuid import uuid4
from database import cnn, create_table


class Product:

    def __init__(self, name : str, price : Decimal):

        # Fail before create de object rule

        if not name:
            raise ValueError("O nome do produto é obrigatório")

        self.id = str(uuid4())
        self.name = name
        self.price = price


  
    