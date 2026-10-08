import sqlite3


cnn = sqlite3.connect("stock.db", timeout=30.0, isolation_level=None)


def create_table():

    cursor = cnn.cursor()

    tables = {
        'products': ("""
            id UUID PRIMARY KEY NOT NULL,
            unique_ref TEXT UNIQUE NOT NULL,
            name TEXT UNIQUE NOT NULL,
            price NUMERIC(10,2)  NOT NULL CHECK(price >= 0),
            active BOOLEAN NOT NULL DEFAULT TRUE
        """),

        'stocks': ("""id UUID PRIMARY KEY,
                    product_id UUID NOT NULL UNIQUE,
                    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
                    FOREIGN KEY (product_id) REFERENCES products(id)"""),

        'movements' : ("""
                       id UUID PRIMARY KEY NOT NULL,
                       product_id UUID NOT NULL,
                       type TEXT,
                       note TEXT DEFAULT NULL,
                       quantity_moved INTEGER DEFAULT 0,
                       FOREIGN KEY (product_id) REFERENCES products(id)""")
        }
    
    try:

        for table_name, fields in tables.items():
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({fields})")

    except Exception as e:
        print("Houve um erro ao criar a tabela de produtos: ", e)

    finally:
        cursor.close()
