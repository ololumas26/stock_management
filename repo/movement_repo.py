

class MovementsRepository:

    def __init__(self, db_connection):
        self.db = db_connection

    def get_all(self):

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM movements")
            return cursor.fetchall()
        except Exception as error:
            raise RuntimeError("Erro ao buscar movimentações") from error

    def get_by_id(self, movement_id):

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM movements WHERE id = ?", (movement_id,))
            return cursor.fetchone()
        except Exception as error:
            raise RuntimeError("Erro ao buscar movimentação") from error

    def create(self, movement):

        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO movements (product_id, quantity, movement_type) VALUES (?, ?, ?)",
                (movement["product_id"], movement["quantity"], movement["movement_type"]),
            )
            self.db.commit()
            return cursor.lastrowid
        except Exception as error:
            self.db.rollback()
            raise RuntimeError("Erro ao criar movimentação") from error

    def update(self, movement_id, movement):

        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE movements SET product_id = ?, quantity = ?, movement_type = ? WHERE id = ?",
                (movement["product_id"], movement["quantity"], movement["movement_type"], movement_id),
            )
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as error:
            self.db.rollback()
            raise RuntimeError("Erro ao atualizar movimentação") from error

    def delete(self, movement_id):
        
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM movements WHERE id = ?", (movement_id,))
            self.db.commit()
            return cursor.rowcount > 0
        except Exception as error:
            self.db.rollback()
            raise RuntimeError("Erro ao excluir movimentação") from error

        