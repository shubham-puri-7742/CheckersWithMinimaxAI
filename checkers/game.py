# the game class - with the core gameplay logic
import pygame
from .constants import BLACK, WHITE, RED, SQUARE_SIZE
from .board import Board

class Game:
  # ctor
  def __init__(self, win):
    # initialise the game state
    self._init()
    # set the active window
    self.win = win

  # update the board
  def update(self):
    self.board.draw(self.win)
    self.drawValidMoves(self.validMoves)
    pygame.display.update()

  # private game state initialiser
  def _init(self):
    # nothing selected initially
    self.selected = None
    # initialise a board
    self.board = Board()
    # begin with black's turn
    self.turn = BLACK
    # initialise a blank dictionary of valid moves
    self.validMoves = {}

  def winner(self):
    return self.board.winner()

  # resets the game state
  def reset(self):
    self._init()

  # select a row and col
  def select(self, row, col):
    # if something is selected
    if self.selected:
      # move it to row, col
      result = self._move(row, col)

      # if invalid
      if not result:
        # reset the selection
        self.selected = None
        self.select(row, col)

    # select the piece at row, col
    piece = self.board.getPiece(row, col)
    # if it is the current player's piece
    if piece != 0 and piece.colour == self.turn:
      # select it
      self.selected = piece
      # get its valid moves
      self.validMoves = self.board.getValidMoves(piece)
      return True

    return False    
  
  # privately move to row, col
  def _move (self, row, col):
    # get the piece at row, col
    piece = self.board.getPiece(row, col)
    # if we have something selected and an empty square from valid moves is clicked
    if self.selected and piece == 0 and (row, col) in self.validMoves:
      # move the selected piece there
      self.board.movePiece(self.selected, row, col)
      # get the skipped pieces for the played move
      skipped = self.validMoves[(row, col)]
      # if we skipped a piece
      if skipped:
        # remove it
        self.board.remove(skipped)
      # alternate turns
      self.changeTurn()
    else:
      return False
    
    return True

  def drawValidMoves(self, moves):
    # for each valid move
    for move in moves:
      # get destination row, col
      row, col = move
      # draw a radius 50 circle there to indicate a valid move. Offset by SQUARE_SIZE // 2 to centre things.
      pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
  
  # alternate turns
  def changeTurn(self):
    # clear valid moves (erase the displayed moves)
    self.validMoves = {}
    if self.turn == BLACK:
      self.turn = WHITE
    else:
      self.turn = BLACK

  # gets the board
  def getBoard(self):
    return self.board

  # Plays the AI's move
  def AImove(self, board):
    # Hackish: we simply change the board (See Minimax implementation)
    self.board = board
    # and change turns
    self.changeTurn()