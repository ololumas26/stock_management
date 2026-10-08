from model.stock import Stock
from repo.stock_repo import StockRepository
from service.product_service import ProductService


class StockService:

    def __init__(self, db_connection):
        
        self.stock_repo = StockRepository(db_connection)
        self.product_service = ProductService(db_connection)

    def create(self, stock : Stock):

        if not self.product_service.get_by_id(stock.product_id):
            raise ValueError("Product not found")

        return self.stock_repo.save(stock)