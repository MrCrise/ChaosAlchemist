from src.components import Transform, Velocity, State, Sprite, InputTag
from src.ecs import System, Component
import pygame


class StateSystem(System):
    def __init__(self):
        super().__init__()
        self.required_components = [State]

    def update(self, dt: float) -> None:
        for entity in self.entities:
            state_comp: Component = entity.get_component(State)

            current_state_key: str = state_comp.current

            current_state = state_comp.states.get(current_state_key)
            if not current_state:
                print(f'Invalid current state: {current_state_key}')
                continue

            new_state = current_state.update(entity, dt)

            if (new_state is not None) and (new_state in state_comp.states):
                self._change_state(entity, state_comp, new_state)

    def handle_event(self, event) -> None:
        for entity in self.entities:
            state_comp: Component = entity.get_component(State)

            current_state_key: str = state_comp.current

            current_state = state_comp.states.get(current_state_key)
            if not current_state:
                print(f'Invalid current state: {current_state_key}')
                continue

            new_state = current_state.handle_event(entity, event)

            if new_state:
                self._change_state(entity, state_comp, new_state)

    def _change_state(self, entity, state_comp, new_state_key):
        '''State switch method.'''
        if new_state_key not in state_comp.states:
            print(f"Attempt to switch to invalid state: {new_state_key}")
            return

        state_comp.states[state_comp.current].exit(entity)
        state_comp.current = new_state_key
        state_comp.states[new_state_key].enter(entity)


class InputSystem(System):
    def __init__(self):
        super().__init__()
        self.required_components = [InputTag]

    def update(self, dt):
        keys = pygame.key.get_pressed()

        for entity in self.entities:
            self._handle_movement_input(entity, keys)
            self._handle_attack_input(entity)

    def _handle_movement_input(self, entity, keys):
        velocity = entity.get_component(Velocity)

        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        direction = pygame.Vector2(dx, dy)

        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.Vector2()
        velocity.direction = direction

    def _handle_attack_input(self, entity):

        # TODO: Implement attacking.

        mouse = pygame.mouse.get_pressed()

        if mouse[0]:
            print('Attack handled!')


class MovementSystem(System):
    def __init__(self):
        super().__init__()
        self.required_components = [Transform, Velocity]

    def update(self, dt: float) -> None:
        for entity in self.entities:
            transform = entity.get_component(Transform)
            velocity = entity.get_component(Velocity)

            transform.rect.center += velocity.direction * velocity.speed * dt

            # Limit exiting beyond the screen.
            transform.rect.clamp_ip(pygame.Rect(0, 0, 1920, 1080))


class RenderSystem(System):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.required_components = [Transform, Sprite]

    def update(self, dt: float) -> None:
        self.screen.fill('darkgray')
        for entity in self.entities:
            transform = entity.get_component(Transform)
            sprite = entity.get_component(Sprite)
            self.screen.blit(sprite.surface, transform.rect)
