from decimal import Decimal
from uuid import uuid4
from database import cnn, create_table



class Product:

    def __init__(self, name : str, price : Decimal, quantity : int = 0, note : str = ""):

        # Fail before create de object rule

        if not name:
            raise ValueError("O nome do produto é obrigatório")

        self.id = str(uuid4())
        self.unique_ref = str('PDK-'+ self.id[4:10]) # Alterar depois para algo com significado semantico
        self.name = name
        self.price = price

        self.quantity = quantity
        self.note = note = note


  
    