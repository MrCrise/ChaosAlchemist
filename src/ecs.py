class Component:
    pass


class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component):
        return self.components.get(component)


class System:
    def __init__(self):
        self.entities = []
        self.required_components = []

    def register_entity(self, entity):
        if self._check_requirements(entity):
            self.entities.append(entity)

    def _check_requirements(self, entity):
        required = self.required_components
        return all(t in entity.components for t in required)

    def update(self, dt):
        pass
