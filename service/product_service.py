from repo.product_repo import ProductRepository
from model.product import Product
from model.moviment import Movements, MovimentsType
from model.stock import Stock

class ProductService:

    def __init__(self, db_connection):

        # self.db_cnn = db_connection
        self.product_repo : ProductRepository = ProductRepository(db_connection)

    def create_product(self, product : Product):

        stock = Stock(product.id, quantity=product.quantity)
        mov = Movements(product.id, mov_type=MovimentsType.ENTRANCE.value)

        return self.product_repo.save(product=product, stock=stock, movement=mov)

    def get_all(self, page : int = 1, limit : int = 10):
        offset = (page - 1) * limit
        return self.product_repo.get_all(limit=limit, offset=offset)
    
    def get_by_id(self, product_id : str):
        return self.product_repo.get_by_id(product_id=product_id)

    def get_by_name(self, product_name : str):
        return self.product_repo.get_by_name(product_name)
