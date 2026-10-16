import sqlite3
import unittest
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from tempfile import NamedTemporaryFile

from database import create_connection
from migrations.runner import run_migrations
from model.product import Product
from service.product_service import ProductService
from service.stock_service import StockService


class TestStockService(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:", isolation_level=None)
        self.connection.execute("PRAGMA foreign_keys = ON")
        run_migrations(self.connection)

        self.product_service = ProductService(self.connection)
        self.stock_service = StockService(self.connection)

        self.product = Product("Monitor", Decimal("199.90"), quantity=10)
        self.product_service.create_product(self.product)

    def tearDown(self):
        self.connection.close()

    def get_quantity(self):
        return self.connection.execute(
            "SELECT quantity FROM stocks WHERE product_id = ?",
            (self.product.id,),
        ).fetchone()[0]

    def get_movement_count(self):
        return self.connection.execute(
            "SELECT COUNT(*) FROM movements WHERE product_id = ?",
            (self.product.id,),
        ).fetchone()[0]

    def test_register_entrance_increases_stock_and_creates_movement(self):
        self.stock_service.regist_entrance(self.product.id, 5, "Reposição")

        self.assertEqual(self.get_quantity(), 15)
        self.assertEqual(self.get_movement_count(), 2)

    def test_register_exit_decreases_stock_and_creates_movement(self):
        self.stock_service.regist_exit(self.product.id, 4, "Venda")

        self.assertEqual(self.get_quantity(), 6)
        self.assertEqual(self.get_movement_count(), 2)

    def test_exit_with_insufficient_stock_does_not_change_stock_or_history(self):
        with self.assertRaises(ValueError):
            self.stock_service.regist_exit(self.product.id, 11)

        self.assertEqual(self.get_quantity(), 10)
        self.assertEqual(self.get_movement_count(), 1)

    def test_non_positive_quantity_is_rejected(self):
        with self.assertRaises(RuntimeError):
            self.stock_service.regist_entrance(self.product.id, 0)

        with self.assertRaises(RuntimeError):
            self.stock_service.regist_exit(self.product.id, -1)

        self.assertEqual(self.get_quantity(), 10)
        self.assertEqual(self.get_movement_count(), 1)

    def test_movement_failure_rolls_back_stock_update(self):
        self.connection.execute(
            f"""
            CREATE TRIGGER reject_product_movement
            BEFORE INSERT ON movements
            WHEN NEW.product_id = '{self.product.id}'
            BEGIN
                SELECT RAISE(ABORT, 'forced movement failure');
            END;
            """
        )

        with self.assertRaises(Exception):
            self.stock_service.regist_entrance(self.product.id, 5)

        self.assertEqual(self.get_quantity(), 10)
        self.assertEqual(self.get_movement_count(), 1)

    def test_concurrent_exits_do_not_oversell_stock(self):
        with NamedTemporaryFile(suffix=".db") as database_file:
            database_path = database_file.name
            connection = create_connection(database_path)
            run_migrations(connection)

            product = Product("Concurrent monitor", Decimal("199.90"), quantity=10)
            ProductService(connection).create_product(product)
            connection.close()

            def register_exit():
                worker_connection = create_connection(database_path)
                try:
                    try:
                        return StockService(worker_connection).regist_exit(
                            product.id,
                            7,
                        )
                    except ValueError as error:
                        return error
                finally:
                    worker_connection.close()

            with ThreadPoolExecutor(max_workers=2) as executor:
                results = list(executor.map(lambda _: register_exit(), range(2)))

            verification_connection = create_connection(database_path)
            try:
                quantity = verification_connection.execute(
                    "SELECT quantity FROM stocks WHERE product_id = ?",
                    (product.id,),
                ).fetchone()[0]
            finally:
                verification_connection.close()

            self.assertEqual(results.count(True), 1)
            self.assertEqual(sum(isinstance(result, ValueError) for result in results), 1)
            self.assertEqual(quantity, 3)


if __name__ == "__main__":
    unittest.main()
