from service.product_service import ProductService
from model.product import Product
from model.stock import Stock
from database import create_table, cnn

from service.stock_service import StockService
from service.movement_service import MovementService

from repo.movement_repo import MovementsRepository
from service.dashboard_service import DashboardService


# create_table()

# p = Product("Iphone 18", 608, 20)
# service = ProductService(cnn)

s = StockService(cnn)
s.regist_entrance('0567ca4a-b097-4936-80d4-c65730c402e5', 5)
# s.regist_entrance('e0cddbef-6490-451a-9e2b-4e29dcc20173', 5)



# movements = MovementService(cnn)
# mov_repo = MovementsRepository(cnn)

# print(movements.get_all_movements())
# # print(mov_repo.get_total_movements())



# dashboard = DashboardService(cnn)
# print(dashboard.get_summary())