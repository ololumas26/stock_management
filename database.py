import sqlite3

cnn = sqlite3.connect("stock.db")


def create_table():

    cursor = cnn.cursor()
    try:

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS products(
                    id UUID, name TEXT, price FLOAT, quantity INTEGER
                )
            """)

    except Exception as e:
        print("Houve um erro ao criar a tabela de produtos: ", e)

    finally:
        cursor.close()
