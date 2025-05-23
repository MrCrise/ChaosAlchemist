from src.ecs import Component
from pygame import Vector2, image, Surface, Rect
import pygame
from typing import Optional, Dict


class State(Component):
    '''
    Component that stores data about states of an object.
    '''

    def __init__(self, initial_states: Optional[dict] = None):
        self.states: dict = initial_states if initial_states is not None else {}


class InputTag(Component):
    '''
    Tag that the entity can handle input.
    '''
    pass


class Collider(Component):
    '''
    Tag that the entity needs to be collided.
    Also stores info about collision type.
    '''

    def __init__(self, collision_types: list = ['solid']):
        # True if entity shouldn't block movement.
        self.collision_types = collision_types


class Transform(Component):
    '''
    Component that stores position, rotation and scale of an object.
    '''

    def __init__(self,
                 rect: Optional[Rect] = None,
                 inflate_by: Optional[tuple] = None):

        self.rect: Rect = rect if rect else Rect(0, 0, 32, 32)
        self.hitbox: Rect = rect.copy() if inflate_by is None else rect.inflate(*inflate_by)
        self.rotation: float = 0.0
        self.scale: Vector2 = Vector2(1, 1)


class Velocity(Component):
    '''
    Component that stores object movement.
    '''

    def __init__(self, speed: float = 0.0):
        self.speed: float = speed
        self.direction: Vector2 = Vector2(0, 0)
        self.max_speed: Optional[float] = None


class Sprite(Component):
    '''
    Component that stores visual representation of an object.
    '''

    def __init__(self,
                 image_path: Optional[str] = None,
                 color: tuple = (255, 255, 255),
                 size: tuple = (32, 32)):

        self.image_path: Optional[str] = image_path
        self.color: tuple = color
        self.size: tuple = size
        self.surface: Surface = self._load_surface()
        self.mask = pygame.mask.from_surface(self.surface)
        self.visible: bool = True

    def _load_surface(self) -> Surface:
        if self.image_path:
            return image.load(self.image_path).convert_alpha()
        surf = Surface(self.size)
        surf.fill(self.color)
        return surf


class Animation(Component):
    '''
    Component that stores animation data of an object.
    '''

    def __init__(self,
                 animations: dict = {},
                 current_animation: str = 'idle',
                 time_passed: float = 0,
                 current_frame: int = 0):

        self.animations: dict = animations
        self.current_animation: str = current_animation
        self.time_passed: float = time_passed
        self.current_frame: int = current_frame


class Health(Component):
    '''
    Component that stores health of an object.
    '''

    def __init__(self, max_hp: int = 100):
        self.max_hp: int = max_hp
        self.current_hp: int = max_hp
        self.invulnerable: bool = False
        self.invulnerability_timer: float = 0.0
