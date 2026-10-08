from uuid import uuid4


class Stock:

    def __init__(self, product_id : str, quantity : int = 0):

        if quantity < 0:
            raise ValueError("Quantity cannot be less than 0")
        
        self.id = str(uuid4())
        self.product_id = product_id
        self.quantity = quantity