from service.product_service import ProductService
from repo.product_repo import ProductRepository
from model.product import Product
from database import create_table, cnn



create_table()
p = Product("Iphone 16", 10, 10)
service = ProductService(cnn)

service.create_product(p)