from src.components import Transform, Velocity, State, Sprite, InputTag, Collider, Animation
from src.ecs import System, Component, Entity
from src.events import CollisionEvent
from src.states import IdleState, MovingState
import pygame


class StateSystem(System):
    '''
    System that changes the states of entities.
    '''

    def __init__(self):
        super().__init__()
        self.required_components = [State]

    def update(self, dt: float) -> None:
        for entity in self.entities:
            state_comp: Component = entity.get_component(State)

            current_states_status: list = state_comp.states

            if 'idle' in current_states_status and 'moving' in current_states_status:
                self._handle_movement_states(entity, current_states_status)

    def _handle_movement_states(self, entity, current_states_status) -> None:
        velocity = entity.get_component(Velocity)

        is_idling = current_states_status['idle']
        moving_directions = set()

        if velocity.direction.length() > 0:
            is_idling = False

            if velocity.direction.x > 0:
                moving_directions.add('right')
            elif velocity.direction.x < 0:
                moving_directions.add('left')

            if velocity.direction.y > 0:
                moving_directions.add('down')
            elif velocity.direction.y < 0:
                moving_directions.add('up')
        else:
            is_idling = True

        current_states_status['idle'] = is_idling
        current_states_status['moving'] = moving_directions if moving_directions != set(
        ) else None

    def _handle_attacking_states(self, entity):
        pass


class InputSystem(System):
    '''
    System that handles player input.
    '''

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
    '''
    System that handles movement of entities.
    '''

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


class AnimationSystem(System):
    '''
    System that handles animations of entities.
    '''

    def __init__(self):
        super().__init__()
        self.required_components = [Sprite, Animation]

    def update(self, dt: float) -> None:
        for entity in self.entities:
            sprite: Component = entity.get_component(Sprite)
            animation: Component = entity.get_component(Animation)

            if entity.get_component(State) is not None:
                state: Component = entity.get_component(State)
                self._select_animation(animation, state)

            self._update_animation_frame(animation, sprite, dt)

    def _select_animation(self, animation: Component, state: Component):
        if 'moving' in state.states and state.states['moving'] is not None:
            directions = state.states['moving']

            if 'left' in directions and 'move_left' in animation.animations:
                self._set_current_animation(animation, 'move_left')
            elif 'right' in directions and 'move_right' in animation.animations:
                self._set_current_animation(animation, 'move_right')

        elif 'idle' in state.states and state.states['idle']:
            self._set_current_animation(animation, 'idle')

    def _set_current_animation(self, animation: Component, animation_name: str):
        if animation.current_animation != animation_name:
            animation.current_animation = animation_name
            animation.time_passed = 0
            animation.current_frame = 0

    def _update_animation_frame(self, animation: Component, sprite: Component, dt: float):
        if not animation.current_animation:
            return

        current_animation_data = animation.animations.get(
            animation.current_animation)
        if not current_animation_data or not current_animation_data.frames:
            return

        animation.time_passed += dt

        if animation.time_passed >= current_animation_data.frame_duration:
            animation.current_frame += 1
            animation.time_passed = 0

            if animation.current_frame >= len(current_animation_data.frames):
                if current_animation_data.loop:
                    animation.current_frame = 0
                else:
                    # Stay on last frame if animation isn't looped.
                    animation.current_frame -= 1

        current_frame: pygame.Surface = current_animation_data.frames[animation.current_frame]
        sprite.surface = current_frame
        sprite.mask = pygame.mask.from_surface(current_frame)


class CollisionDetectionSystem(System):
    '''
    System that detects collisions between entities and stores it as events.
    '''

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
    '''
    System that resolves collision events.
    '''

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
    '''
    System that visualises entities on screen.
    '''

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
