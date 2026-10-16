import sqlite3
import unittest
from decimal import Decimal

from migrations.runner import run_migrations
from model.product import Product
from service.product_service import ProductService


class TestProductService(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:", isolation_level=None)
        self.connection.execute("PRAGMA foreign_keys = ON")
        run_migrations(self.connection)
        self.service = ProductService(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_create_product_persists_product_stock_and_initial_movement(self):
        product = Product("Keyboard", Decimal("49.90"), quantity=0)

        result = self.service.create_product(product)

        self.assertTrue(result)
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM products").fetchone()[0],
            1,
        )
        self.assertEqual(
            self.connection.execute("SELECT quantity FROM stocks").fetchone()[0],
            0,
        )
        self.assertEqual(
            self.connection.execute(
                "SELECT mov_type, quantity_moved FROM movements"
            ).fetchone(),
            ("entrance", 0),
        )

    def test_create_product_rolls_back_when_persistence_fails(self):
        product = Product("Mouse", Decimal("19.90"), quantity=3)

        self.service.create_product(product)

        with self.assertRaises(Exception):
            self.service.create_product(product)

        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM products").fetchone()[0],
            1,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM stocks").fetchone()[0],
            1,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM movements").fetchone()[0],
            1,
        )


if __name__ == "__main__":
    unittest.main()
