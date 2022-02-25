import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK
from checkers.game import Game

FPS = 60

# setup pygame display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def getRowColFromMouse(pos):
  # get mouse x, y from the argument
  x, y = pos
  # get row and column from x, y
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def main():
  run = True

  # for framerate independence
  clock = pygame.time.Clock()
  # iniitalise a game instance
  game = Game(WIN)

  # game loop
  while run:
    clock.tick(FPS)
    
    # if someone won
    if game.winner() != None:
      # print the colour of the winner
      print(game.winner())
      input()
      run = False

    # query for events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      # process clicks
      if event.type == pygame.MOUSEBUTTONDOWN:
        # get the mouse position
        pos = pygame.mouse.get_pos()
        # get the corresponding row and col
        row, col = getRowColFromMouse(pos)
        game.select(row, col)

    game.update()

  pygame.quit()

main()