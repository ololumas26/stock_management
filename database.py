import sqlite3


# cnn = sqlite3.connect("stock.db", timeout=30.0, isolation_level=None)
# cnn.execute("PRAGMA foreign_keys = ON") # Habilita as chaves estrangeiras

def create_connection(path = "stock.db"):

    if not path:
        raise RuntimeError("Database name is required")

    cnn = sqlite3.connect(path, timeout=30.0, isolation_level=None)
    cnn.execute("PRAGMA foreign_keys = ON")

    return cnn
