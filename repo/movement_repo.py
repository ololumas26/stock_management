

class MovementsRepository:

    def __init__(self, db_connection):
        self.db = db_connection

    
    def get_by_id(self, movement_id):

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM movements WHERE id = ?", (movement_id,))
            return cursor.fetchone()
        except Exception as error:
            raise RuntimeError("Error getting movement") from error

    def get_all(self, limit : int, offset : int):

        cursor = self.db.cursor()
        try:
            return cursor.execute("SELECT * FROM movements limit ? offset ?", (limit, offset)).fetchall()

        except Exception as e:
            print("An error occurs while getting movements")
            raise

        finally:
            cursor.close()

    def get_total_movements(self):
        
        cursor = self.db.cursor()
        try:
            return cursor.execute("SELECT COUNT(id) from movements").fetchone()

        except Exception as e:
            print("An error occurs while getting movements")
            raise

        finally:
            cursor.close()

    def create(self, movement):

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """
                INSERT INTO movements
                    (id, product_id, mov_type, quantity_moved, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    movement.id,
                    movement.product_id,
                    movement.mov_type,
                    movement.quantity,
                    movement.note,
                ),
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
                """
                UPDATE movements
                SET product_id = ?, mov_type = ?, quantity_moved = ?, note = ?
                WHERE id = ?
                """,
                (
                    movement.product_id,
                    movement.mov_type,
                    movement.quantity,
                    movement.note,
                    movement_id,
                ),
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

        
