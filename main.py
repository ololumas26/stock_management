from service.product_service import ProductService
from model.product import Product
from model.stock import Stock
from database import create_table, cnn

from service.stock_service import StockService



create_table()

p = Product("Iphone 18", 608, 20)
service = ProductService(cnn)

s = StockService(cnn)
# s.regist_entrance('0567ca4a-b097-4936-80d4-c65730c402e5', 5)
s.regist_exit('0567ca4a-b097-4936-80d4-c65730c402e5', 3)


