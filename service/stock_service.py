from model.stock import Stock
from repo.stock_repo import StockRepository
from service.product_service import ProductService
from model.moviment import MovimentsType, Movements
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


    def regist_stock(self, product_id : str, quantity : int, t : MovimentsType, note : str = ''):

        if quantity <= 0:
            raise RuntimeError("Quantity to move should be greater than ZERO (0)")
  
        mov = Movements(product_id, t.value,quantity, note)

        return self.stock_repo.regist_new_stock(product_id=product_id,quantity=quantity,movement=mov)
    

    # Mudar a forma como registo o stock e passar a registar de forma atomica para que também possa registar o movimento de
    # Entrada ou saída na mesma transação.
    
    def regist_entrance(self, product_id : str, quantity : int, note : str = ''):
        return self.regist_stock(product_id=product_id, quantity=quantity, t=MovimentsType.ENTRANCE, note = note)
    

    def regist_exit(self, product_id : str, quantity : int, note : str = ''):
        return self.regist_stock(product_id=product_id, quantity=quantity, t=MovimentsType.EXIT, note=note)
       