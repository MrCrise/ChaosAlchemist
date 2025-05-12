from typing import Optional
from src.ecs import Entity
from src.components import *
from src.states import *


class Player(Entity):
    def __init__(self,
                 sprite_image_path: Optional[str] = None,
                 size: Optional[tuple] = None,
                 starting_pos: tuple = (0, 0)):
        super().__init__()

        self.add_component(Sprite(sprite_image_path))
        self.add_component(
            Transform(
                rect=self.get_component(
                    Sprite).surface.get_rect(center=starting_pos),
                inflate_by=(0, 0)
            )
        )
        self.add_component(Velocity(500))
        self.add_component(Health(100))
        self.add_component(InputTag())
        self.add_component(Collider())

        possible_states = {
            'idle': True,
            'moving': set(),
        }
        self.add_component(State(possible_states))


class Obstacle(Entity):
    def __init__(self,
                 sprite_image_path: Optional[str] = None,
                 size: Optional[tuple] = None,
                 starting_pos: tuple = (0, 0)):
        super().__init__()

        self.add_component(Sprite(size=size, color=(0, 0, 255)))
        self.add_component(
            Transform(
                rect=self.get_component(
                    Sprite).surface.get_rect(center=starting_pos)
            )
        )
        self.add_component(Collider())
