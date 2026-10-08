from repo.product_repo import ProductRepository
from model.product import Product


class ProductService:

    def __init__(self, db_connection):

        # self.db_cnn = db_connection
        self.product_repo : ProductRepository = ProductRepository(db_connection)


    def create_product(self, product : Product):
        self.product_repo.save(product=product)
        
    
