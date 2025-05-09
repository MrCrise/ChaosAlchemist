from src.components import Transform, Velocity, State, Sprite, InputTag, Collider
from src.ecs import System, Component, Entity
from src.events import CollisionEvent
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

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        for entity in self.entities:
            self._handle_movement_input(entity, keys)
            self._handle_attack_input(entity)

    def _handle_movement_input(self, entity: Entity, keys) -> None:
        velocity = entity.get_component(Velocity)

        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        direction = pygame.Vector2(dx, dy)

        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.Vector2()
        velocity.direction = direction

    def _handle_attack_input(self, entity: Entity) -> None:

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

            transform.hitbox.center += velocity.direction * velocity.speed * dt

            # Limit exiting beyond the screen.
            transform.hitbox.clamp_ip(pygame.Rect(0, 0, 1920, 1080))

            transform.rect.center = transform.hitbox.center


class CollisionDetectionSystem(System):
    def __init__(self):
        super().__init__()
        self.required_components = [Collider, Transform]
        # Stores collision events per frame.
        self.events: list[CollisionEvent] = []

    def update(self, dt: float) -> None:
        self.events.clear()

        for ent_a in self.entities:
            # Get only entities that can move.
            if not (Velocity in ent_a.components):
                continue
            for ent_b in self.entities:
                if ent_a == ent_b:
                    continue

                col_a = ent_a.get_component(Collider)
                col_b = ent_b.get_component(Collider)

                # Check only solid to solid collisions.
                if 'solid' in col_a.collision_types and 'solid' in col_b.collision_types:
                    trans_a = ent_a.get_component(Transform)
                    trans_b = ent_b.get_component(Transform)

                    if trans_a.hitbox.colliderect(trans_b.hitbox):
                        self.events.append(CollisionEvent(ent_a, ent_b))

                # TODO: Implement other collision type checks.
                #       For example: solid to non solid


class CollisionResolutionSystem(System):
    def __init__(self, detection_system: CollisionDetectionSystem):
        super().__init__()
        self.required_components = [Collider, Transform]
        self.detection_system = detection_system

    def update(self, dt: float) -> None:
        for event in self.detection_system.events:
            ent_a, ent_b = event.entity_a, event.entity_b
            if not (Transform in ent_a.components) or not (Velocity in ent_a.components):
                continue

            trans_a = ent_a.get_component(Transform)
            trans_b = ent_b.get_component(Transform)

            dx = trans_a.hitbox.centerx - trans_b.hitbox.centerx
            dy = trans_a.hitbox.centery - trans_b.hitbox.centery

            overlap_x = (trans_a.hitbox.width +
                         trans_b.hitbox.width) / 2 - abs(dx)
            overlap_y = (trans_a.hitbox.height +
                         trans_b.hitbox.height) / 2 - abs(dy)

            if overlap_x < overlap_y:
                sign = 1 if dx > 0 else -1
                trans_a.hitbox.x += sign * overlap_x
            else:
                sign = 1 if dy > 0 else -1
                trans_a.hitbox.y += sign * overlap_y

            trans_a.rect.center = trans_a.hitbox.center


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
