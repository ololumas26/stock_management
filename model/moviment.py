import enum
from uuid import uuid4

class MovimentsType(enum.Enum):
    ENTRANCE = 'entrance'
    EXIT = 'exit'



class Movements:

    def __init__(self, product_id : str, mov_type : MovimentsType ,quantity : int = 0, note : str = ""):

        self.id = str(uuid4())
        self.product_id = product_id
        self.mov_type = mov_type
        self.quantity = quantity
        self.note = note