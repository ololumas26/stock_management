import sqlite3

cnn = sqlite3.connect("stock.db")


def create_table():

    cursor = cnn.cursor()

    tables = {
        'products': ('id UUID PRIMARY KEY NOT NULL, name TEXT NOT NULL, price FLOAT NOT NULL'),
        'stock': ("""id UUID PRIMARY KEY,
                    product_id UUID NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE""")
        }
    
    try:

        for table_name, fields in tables.items():
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({fields})")

    except Exception as e:
        print("Houve um erro ao criar a tabela de produtos: ", e)

    finally:
        cursor.close()
