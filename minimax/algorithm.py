# the main algorithm script for the minimax algorithm

# for deepcopying (copying the object and not just a reference) the board
from copy import deepcopy
import pygame

# constants: RGB colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# args: current position (board), tree depth, maximising/minimising player, game instant
def minimax(position, depth, maxPlayer, game):
  # BASE CASE
  # we only evaluate at the final leaves
  # if at the final leaf in the branch or someone has won
  if depth == 0 or position.winner() != None:
    # return the evaluation and the corresponding position
    return position.evaluateBoard(), position

  # RECURSIVE LOGIC
  # if maximising the score (WHITE'S TURN)
  if maxPlayer:
    # initialise to - infinity (because we are maximising)
    maxEval = float('-inf')
    # no best move known yet
    bestMove = None
    # for each valid move in the current position (board state)
    for move in getAllMoves(position, WHITE, game):
      # Traverse deeper into the tree. Carry the altered board state for the hypothetical move and alternate turns at each step
      # [0] because the function returns both the evaluation and the move (see return below)
      evaluation = minimax(move, depth - 1, False, game)[0]
      # pick the larger of maxEval (best so far) and evaluation (current one)
      maxEval = max(maxEval, evaluation)
      # if the current evaluation is the best so far
      if maxEval == evaluation:
        # the current move is the best so far
        bestMove = move
    # return the evaluation and the corresponding move
    return maxEval, bestMove
  # if minimising the score (BLACK'S TURN)
  else:
    # initialise to infinity (because we are minimising)
    minEval = float('inf')
    # no best move known yet
    bestMove = None
    # for each valid move in the current position (board state)
    for move in getAllMoves(position, BLACK, game):
      # Traverse deeper into the tree. Carry the altered board state for the hypothetical move and alternate turns at each step
      # [0] because the function returns both the evaluation and the move (see return below)
      evaluation = minimax(move, depth - 1, True, game)[0]
      # pick the smaller of minEval (best so far) and evaluation (current one)
      minEval = min(minEval, evaluation)
      # if the current evaluation is the best so far
      if minEval == evaluation:
        # the current move is the best so far
        bestMove = move
    # return the evaluation and the corresponding move
    return minEval, bestMove

# simulates the move. Only use with copies to avoid 'cheating' in the actual game board
def simulateMove(piece, move, board, game, skip):
  # play the move on the passed board. move is (row, col), so we need to split it
  board.movePiece(piece, move[0], move[1])
  # if we skipped something
  if skip:
    # remove it from the board
    board.remove(skip)
  return board

# get all valid moves from the current position
def getAllMoves(board, colour, game):
  # initialise empty list
  # this will be a list of lists having pairs of board states and (if we want to draw it) corresponding move
  moves = []
  # for each piece of the given colour
  for piece in board.getAllPieces(colour):
    # get all valid moves for the piece
    validMoves = board.getValidMoves(piece)
    # for each key-val pair in the valid moves
    # the items will be a dictionary where the key is the square the piece moves to and the value is a list of all pieces we'd have to skip to get there
    for move, skip in validMoves.items():
      # deepcopy the board because we are modifying a hypothetical 'thought-copy' of the board
      tempBoard = deepcopy(board)
      # temp piece to avoid moving the 'real' pieces in our 'thought-copy'
      tempPiece = tempBoard.getPiece(piece.row, piece.col)
      # simulate the move on a 'thought-copy' of the board
      newBoard = simulateMove(tempPiece, move, tempBoard, game, skip)
      # store that move
      moves.append(newBoard)

  return moves