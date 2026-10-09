from repo.movement_repo import MovementsRepository
from repo.stock_repo import StockRepository
from repo.product_repo import ProductRepository


class DashboardRepository:

    def __init__(self, db_connection):
        self.db = db_connection
        self.stock_repo = StockRepository(db_connection)
        self.product_repo = ProductRepository(db_connection)
        self.movements_repo = MovementsRepository(db_connection)


    def get_summary(self):
        return self.product_repo.get_total_products()
