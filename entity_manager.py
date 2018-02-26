class EntityManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if EntityManager._instance is None:
            EntityManager._instance = object.__new__(cls)
        return EntityManager._instance

    def __init__(self):
        self._map = dict()

    def register_entity(self, entity):
        self._map[entity.id] = entity

    def remove_entity(self, entity):
        self._map.pop(entity.id)

    def get_entity_from_id(self, id):
        return self._map[id]

    # Implements iteration protocol to iterate
    # over entities registered
    def __iter__(self):
        for k in self._map:
            yield self._map[k]
