import pygame

from src.systems import MovementSystem, RenderSystem, InputSystem, CollisionDetectionSystem, CollisionResolutionSystem


class Game:
    '''
    Class for handling main game logic.
    '''

    def __init__(self, screen):
        self.screen = screen
        self.is_paused = False
        self.game_speed = 1.0

        input_system = InputSystem()
        movement_system = MovementSystem()
        col_detection_system = CollisionDetectionSystem()
        col_resolution_system = CollisionResolutionSystem(col_detection_system)
        render_system = RenderSystem(screen)
        self.systems = [input_system,
                        movement_system,
                        col_detection_system,
                        col_resolution_system,
                        render_system]
        self.entities = []

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def add_entity(self, entity):
        self.entities.append(entity)
        for system in self.systems:
            system.register_entity(entity)

    def update(self, dt):
        if not self.is_paused:
            scaled_dt = dt * self.game_speed
            for system in self.systems:
                system.update(scaled_dt)
        else:
            self.update_paused_state()

    def update_game_world(self, scaled_dt):
        pass

    def update_paused_state(self):
        pass
