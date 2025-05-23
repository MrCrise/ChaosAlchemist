from abc import abstractmethod
import os
import pygame
from typing import Optional


class AnimationData:
    '''
    Data structure for storing animation information.
    It is not a component, but a helper class for Animation component.
    '''

    def __init__(self,
                 frames: list[pygame.Surface],
                 frame_duration: float = 0.15,
                 loop: bool = True):

        self.frames: list[pygame.Surface] = frames
        self.frame_duration: float = frame_duration
        self.loop: bool = loop


class SpriteLoader:
    '''
    Utility class for loading sprites and animations of different types.
    '''

    @abstractmethod
    def load_sprite_sheet(
                          path: str,
                          sprite_size: tuple[int, int],
                          colorkey: tuple[int, int, int] = None):
        '''
        Load sprites from a spritesheet.

        Args:
            path: path to a spritesheet
            sprite_size: size of a single sprite
            colorkey: color to become transparent

        Returns:
            List of pygame surfaces each containing individual sprite
        '''
        pass

    @abstractmethod
    def load_folder_frames(
                           path: str,
                           prefix: str = '',
                           suffix: str = '.png',
                           colorkey: Optional[tuple[int, int, int]] = None):
        '''
        Load animation from files in a directory.

        Args:
            path: path to a directory containing frames
            prefix: prefix of the frame filenames
            suffix: suffix of the frame filenames
            colorkey: color to become transparent

        Returns:
            List of pygame surfaces in numerical order
            each containing animation frame
        '''
        frames = []

        try:
            frame_files = [f for f in os.listdir(path)]
            frame_files.sort(key=(lambda f: int(f.replace(prefix, '').replace(suffix, ''))))

            for file in frame_files:
                try:
                    frame = pygame.image.load(os.path.join(path, file)).convert_alpha()
                    if colorkey is not None:
                        frame.set_colorkey(colorkey)
                    frames.append(frame)
                except pygame.error as e:
                    print(f'Unable to load image: {file}')
                    print(f'Error: {e}')
        except FileNotFoundError:
            print(f'Path not found: {path}')

        return frames
