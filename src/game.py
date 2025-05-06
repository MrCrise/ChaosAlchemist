import pygame

from src.systems import MovementSystem, RenderSystem, InputSystem


class Game:
    '''Class for handling main game loop.'''

    def __init__(self, screen):
        self.screen = screen
        self.is_paused = False
        self.game_speed = 1.0
        self.systems = [
            InputSystem(),
            MovementSystem(),
            RenderSystem(screen),
        ]
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
