from repo.movement_repo import MovementsRepository
from utils.pagination import calc_pagination

class MovementService:

    def __init__(self, db_connection):
        self.movement_repo = MovementsRepository(db_connection)


    def build_response(self, movements : list ,total_regists : tuple, page : int , total_pages : int):
        return {
            'data': movements,
            'pagination': {
                'page': page,
                'total': total_regists,
                'pages': total_pages
            }
        }

    def get_all_movements(self, page : int = 1, limit : int = 10):
        offset = calc_pagination(page, limit)
        total_regists = self.movement_repo.get_total_movements()[0]
        return self.build_response(
            movements=self.movement_repo.get_all(limit=limit, offset=offset),
            total_regists=total_regists,
            page=page,
            total_pages=(total_regists // limit) 

        )
