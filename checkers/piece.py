# the checkers piece class
import pygame
from .constants import WHITE, BLACK, SQUARE_SIZE, GREY, CROWN

class Piece:
  # padding and border
  PADDING = 15
  OUTLINE = 4

  def __init__(self, row, col, colour):
    # initialise as non-king at (row, col) with the given colour
    self.row = row
    self.col = col
    self.colour = colour
    self.king = False

    # position (coordinates)
    self.x = 0
    self.y = 0
    self.calculatePosition()

  # calculate x, y based on row and col using SQUARE_SIZE
  def calculatePosition(self):
    # coordinate of the row/col + offset (to get the centre)
    self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
    self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

  def makeKing(self):
    self.king = True

  def drawPiece(self, win):
    # SQUARE_SIZE // 2 because we are not calculating the diameter
    radius = SQUARE_SIZE // 2 - self.PADDING
    # draw the outline
    pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
    # draw a circular piece with the given colour at x, y
    pygame.draw.circle(win, self.colour, (self.x, self.y), radius)

    if self.king:
      # blit - place an image. Offset by height and width because the origin is the top-left, as opposed to the centre for circles
      win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

  # move to a new row, col and calculate new coordinates
  def move(self, row, col):
    self.row = row
    self.col = col
    self.calculatePosition()

  # FOR DEBUGGING
  def __repr__(self):
    return str(self.colour)