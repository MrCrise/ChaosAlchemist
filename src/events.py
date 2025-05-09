
class CollisionEvent:
    '''
    Event storing a pair of colliding entities.
    '''

    def __init__(self, entity_a, entity_b):
        self.entity_a = entity_a
        self.entity_b = entity_b
