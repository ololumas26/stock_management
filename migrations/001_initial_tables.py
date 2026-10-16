


def upgrade(connection):
    statements = (
        """
            CREATE TABLE IF NOT EXISTS products(
                id UUID PRIMARY KEY NOT NULL,
                unique_ref TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                price NUMERIC(10,2)  NOT NULL CHECK(price >= 0),
                active BOOLEAN NOT NULL DEFAULT TRUE)
        """,
        """
            CREATE TABLE IF NOT EXISTS stocks(
                id UUID PRIMARY KEY,
                product_id UUID NOT NULL UNIQUE,
                quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
                FOREIGN KEY (product_id) REFERENCES products(id))
        """,
        """
            CREATE TABLE IF NOT EXISTS movements(
                id UUID PRIMARY KEY NOT NULL,
                product_id UUID NOT NULL,
                mov_type TEXT,
                note TEXT DEFAULT NULL,
                quantity_moved INTEGER NOT NULL DEFAULT 0
                    CHECK (quantity_moved >= 0),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id))
        """,
    )

    for statement in statements:
        connection.execute(statement)
