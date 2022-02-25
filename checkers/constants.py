# File containing useful constants
import pygame

# window dimensions
WIDTH, HEIGHT = 800, 800
# board dimensions
ROWS, COLS = 8, 8
# square size
SQUARE_SIZE = WIDTH // COLS

# colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets\crown.png'), (44, 25))
