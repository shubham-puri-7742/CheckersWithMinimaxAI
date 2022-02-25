# the board class
import pygame
from .constants import ROWS, COLS, BLACK, WHITE, SQUARE_SIZE
from .piece import Piece

class Board:
  def __init__(self):
    # internally, a board is a 2D list (a list of lists)
    self.board = []
    # pieces left on either side
    self.blackLeft = self.whiteLeft = 12
    # number of kings
    self.blackKings = self.whiteKings = 0
    # create the internal representation of the board
    self.createBoard()

  # draws checkerboard on the window (visual representation of the board)
  def drawCheckerboard(self, win):
    # fill with black
    win.fill(BLACK)
    # populate rows
    for row in range(ROWS):
      # populate squares, alternating between colours (checkerboard)
      for col in range(row % 2, COLS, 2):
        # draw a white SQUARE_SIZE x SQUARE_SIZE rectangle at (x, y) = (row * SQUARE_SIZE, col * SQUARE_SIZE)
        pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

  # move piece to row, col
  def movePiece(self, piece, row, col):
    # swap the values in the internal representation of the board
    self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
    # move the piece
    piece.move(row, col)

    # check for promotion to king (last row)
    # this doesn't break because this executes only after a move
    if row == ROWS - 1 or row == 0:
      piece.makeKing()
      if piece.colour == WHITE:
        self.whiteKings += 1
      else:
        self.blackKings += 1

  def getPiece(self, row, col):
    return self.board[row][col]

  # creates the internal representation of the board
  def createBoard(self):
    for row in range(ROWS):
      # a new list for each row
      self.board.append([])
      for col in range(COLS):
        # condition true only for the squares with the pieces
        # even-numbered (odd-indexed because of 0-indexing) in the first (0th) row
        # odd-numbered (even-indexed because of 0-indexing) in the second (1st) row and so on
        if col % 2 == ((row + 1) % 2):
          # white pieces in the first three rows
          if row < 3:
            self.board[row].append(Piece(row, col, WHITE))
          # black pieces
          elif row > 4:
            self.board[row].append(Piece(row, col, BLACK))
          else:
            # 0 = blank
            self.board[row].append(0)
        else:
          self.board[row].append(0)

  # draw the pieces on the board
  def draw(self, win):
    # Draw the checkerboard
    self.drawCheckerboard(win)
    for row in range(ROWS):
      for col in range(COLS):
        # get a particular square
        piece = self.board[row][col]
        # nonzero = a piece exists. Draw it!
        if piece != 0:
          piece.drawPiece(win)

  def remove(self, pieces):
    # for each piece to be removed
    for piece in pieces:
      # set its square to 0
      self.board[piece.row][piece.col] = 0
      # if a piece was removed
      if piece != 0:
        # if it was black
        if piece.colour == BLACK:
          # decrement the number of black pieces
          self.blackLeft -= 1
        # if it was white
        if piece.colour == WHITE:
          # decrement the number of white pieces
          self.whiteLeft -= 1

  def winner(self):
    # no black left
    if self.blackLeft <= 0:
      # = white won
      return WHITE
    # no white left
    elif self.whiteLeft <= 0:
      # = black won
      return BLACK
    # no one won
    return None

  # gets valid moves for a piece
  def getValidMoves(self, piece):
    # moves are internally a dictionary
    # key = destination, value = any pieces we need to jump over
    moves = {}
    # store directions (left, right)
    left = piece.col - 1
    right = piece.col + 1
    row = piece.row

    # as per Pygame's coordinate system
    # < 0 = up, > 0 = down
    if piece.colour == BLACK or piece.king:
      # update the dic of moves. Row - 1 = upwards up to row 0 (three rows above), in steps of -1 (upwards)
      moves.update(self._moveLeft(row - 1, max(row - 3, -1), -1, piece.colour, left))
      # same for right
      moves.update(self._moveRight(row - 1, max(row - 3, -1), -1, piece.colour, right))

    if piece.colour == WHITE or piece.king:
      # update the dic of moves. Row + 1 = downwards down to row 8 (three rows below), in steps of 1 (downwards)
      moves.update(self._moveLeft(row + 1, min(row + 3, ROWS), 1, piece.colour, left))
      # same for right
      moves.update(self._moveRight(row + 1, min(row + 3, ROWS), 1, piece.colour, right))

    return moves

  # functions to move left and right
  # arguments - self, start, end, step (for the for loop), colour, left/right (starting column), a list of skipped pieces
  def _moveLeft(self, start, stop, step, colour, left, skipped = []):
    # empty dictionary of moves
    moves = {}
    # empty list of last
    last = []
    # args from params
    for r in range(start, stop, step):
      # bounds checking
      if left < 0:
        break

      current = self.board[r][left]
      # If we found an empty square
      if current == 0:
        # We skipped over something and found a blank square, but there is nothing we can jump over again (no chainable move)
        if skipped and not last:  
          break
        # Valid double jump possible
        elif skipped:
          # add the last piece jumped with the skipped piece to the list of pieces we jumped over
          moves[(r, left)] = last + skipped
        else:
          # it is a valid move
          moves[(r, left)] = last

        # if we skipped over something, check if we can chain moves
        if last:
          # if going upwards
          if step == -1:
            # where we stop after the jump
            row = max(r - 3, 0)
          # if going downwards
          else:
            # where we stop after the jump
            row = min(r + 3, ROWS)

          # update moves recursively
          moves.update(self._moveLeft(r + step, row, step, colour, left - 1, skipped = last))
          moves.update(self._moveRight(r + step, row, step, colour, left + 1, skipped = last))
        break

      # If we found a square with the same player's piece
      elif current.colour == colour:
        # no valid move
        break
      # If we found a square with the opponent's piece
      else:
        # we can jump over it (if there's an empty square behind it)
        last = [current]

      # move left (along the diagonal)
      left -= 1

    return moves

  def _moveRight(self, start, stop, step, colour, right, skipped = []):
    # empty dictionary of moves
    moves = {}
    # empty list of last
    last = []
    # args from params
    for r in range(start, stop, step):
      # bounds checking
      if right >= COLS:
        break

      current = self.board[r][right]
      # If we found an empty square
      if current == 0:
        # We skipped over something and found a blank square, but there is nothing we can jump over again (no chainable move)
        if skipped and not last:  
          break
        # Valid double jump possible
        elif skipped:
          # add the last piece jumped with the skipped piece to the list of pieces we jumped over
          moves[(r, right)] = last + skipped
        else:
          # it is a valid move
          moves[(r, right)] = last

        # if we skipped over something, check if we can chain moves
        if last:
          # if going upwards
          if step == -1:
            # where we stop after the jump
            row = max(r - 3, 0)
          # if going downwards
          else:
            # where we stop after the jump
            row = min(r + 3, ROWS)

          # update moves recursively
          moves.update(self._moveLeft(r + step, row, step, colour, right - 1, skipped = last))
          moves.update(self._moveRight(r + step, row, step, colour, right + 1, skipped = last))
        break

      # If we found a square with the same player's piece
      elif current.colour == colour:
        # no valid move
        break
      # If we found a square with the opponent's piece
      else:
        # we can jump over it (if there's an empty square behind it)
        last = [current]

      # move left (along the diagonal)
      right += 1

    return moves