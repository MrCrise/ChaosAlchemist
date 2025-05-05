import pygame
from typing import Optional
from src.components import Velocity


class BaseState:
    '''Base class for states logic (not a state component!).'''
    def enter(self, entity):
        '''Called when an entity enters a state.'''
        pass

    def exit(self, entity):
        '''Called when an entity exits a state.'''
        pass

    def update(self, entity, dt: float) -> Optional[str]:
        '''Updates current state and returns a new state if needed.'''
        return None

    def handle_event(self, entity, event) -> Optional[str]:
        '''Handles events and returns a new state if needed.'''
        return None


class IdleState(BaseState):
    def enter(self, entity):
        entity.get_component(Velocity).speed = 0

    def handle_event(self, entity, event) -> Optional[str]:
        if event.type == pygame.KEYDOWN:
            if any(event.key == k for k in (pygame.K_w, pygame.K_a,
                                            pygame.K_s, pygame.K_d)):
                return 'moving'
            # elif event.key == pygame.K_q:
            #     return 'casting'

        return None


class MovingState(BaseState):
    def enter(self, entity):
        entity.get_component(Velocity).speed = 500.0

    def update(self, entity, dt):
        keys = pygame.key.get_pressed()
        velocity = entity.get_component(Velocity)

        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        direction = pygame.Vector2(dx, dy)

        if direction.length() > 0:
            direction = direction.normalize()
            velocity.direction = direction
        else:
            velocity.direction = pygame.Vector2(0, 0)
            return 'idle'

        return None
