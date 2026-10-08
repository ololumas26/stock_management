from model.stock import Stock
from repo.stock_repo import StockRepository
from service.product_service import ProductService
from model.moviment import MovimentsType
from repo.movement_repo import MovementsRepository

class StockService:

    def __init__(self, db_connection):
        
        self.stock_repo = StockRepository(db_connection)
        self.product_service = ProductService(db_connection)
        self.moviment_repo = MovementsRepository(db_connection)

    def create(self, stock : Stock):

        if not self.product_service.get_by_id(stock.product_id):
            raise ValueError("Product not found")

        return self.stock_repo.save(stock)


    def regist_stock(self, product_id : str, quantity : int, t : MovimentsType):

        product_stock : Stock = self.stock_repo.get_by_product_id(product_id)

        if not product_stock:
            raise ValueError("PRODUCT NOT FOUND")
        
        _, prod_id , quant = product_stock

        if t == MovimentsType.ENTRANCE:
            quant += quantity

        else:
            quant -= quantity

        return self.stock_repo.regist_new_stock(Stock(product_id=prod_id, quantity=quant))
    

    # Mudar a forma como registo o stock e passar a registar de forma atomica para que também possa registar o movimento de
    # Entrada ou saída na mesma transação.
    
    def regist_entrance(self, product_id : str, quantity : int):
        return self.regist_stock(product_id=product_id, quantity=quantity, t=MovimentsType.ENTRANCE)
    

    def regist_exit(self, product_id : str, quantity : int):
        return self.regist_stock(product_id=product_id, quantity=quantity, t=MovimentsType.EXIT)
       