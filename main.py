import pygame
from src.game import Game
from src.entitys import Player, Obstacle
from src.components import Transform, State
from random import randint

FPS = 240
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chaos Alchemist')
    clock = pygame.time.Clock()

    game = Game(screen)

    player = Player('assets/images/player/right/0.png',
                    starting_pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    game.add_entity(player)

    for i in range(10):
        x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
        w, h = randint(50, 100), randint(50, 100)
        obst = Obstacle(None, (w, h), (x, y))
        game.add_entity(obst)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        # print(clock.get_fps())

        print(player.get_component(State).states['moving'])

        pygame.display.set_caption(f'Chaos Alchemist - FPS: {clock.get_fps()}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # game.systems[1].handle_event(event)

        game.update(dt)
        pygame.display.flip()

    pygame.quit()
