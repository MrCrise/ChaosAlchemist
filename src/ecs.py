class Component:
    '''
    Base class for implementing Components.
    '''

    pass


class Entity:
    '''
    Base class for implementing Entities.
    '''

    def __init__(self):
        self.components = {}

    def add_component(self, component) -> None:
        '''Add component to an entity.'''
        self.components[type(component)] = component

    def get_component(self, component) -> Component:
        '''Get component object that the entity has.'''
        return self.components.get(component)


class System:
    '''
    Base class for implementing Systems.
    '''

    def __init__(self):
        self.entities = []
        self.required_components = []

    def register_entity(self, entity) -> None:
        '''Register entity in system.'''
        if self._check_requirements(entity):
            self.entities.append(entity)

    def _check_requirements(self, entity) -> bool:
        '''Check if entity meets the requirements
           for processing by the system.'''
        required = self.required_components
        return all(t in entity.components for t in required)

    def update(self, dt) -> None:
        '''Processes entities registered in the system.'''
        pass
