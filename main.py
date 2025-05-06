import pygame
from src.game import Game
from src.entitys import Player
from src.components import Transform, State


FPS = 165
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chaos Alchemist')
    clock = pygame.time.Clock()

    game = Game(screen)

    player = Player('assets/images/player/down/0.png',
                    (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    game.add_entity(player)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        # print(clock.get_fps())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # game.systems[1].handle_event(event)

        game.update(dt)
        pygame.display.flip()

    pygame.quit()
