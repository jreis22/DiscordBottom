
class BaseRepository:

    def get_by_id(self, id):
        raise NotImplementedError(
            "Implement 'get_by_id' from class 'BaseRepository'")

    def insert(self, entity) -> bool:
        raise NotImplementedError(
            "Implement 'insert' from class 'BaseRepository'")
        
    def update(self, id, entity) -> bool:
        raise NotImplementedError(
            "Implement 'update' from class 'BaseRepository'")

    def has(self, id) -> bool:
        raise NotImplementedError(
            "Implement 'has' from class 'BaseRepository'")