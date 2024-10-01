import StaticEvaluatorRN

import chess
import chess.engine
from chess import Board, pgn

board = chess.Board()
evaluator = StaticEvaluatorRN.StaticEvaluatorRN()
print(evaluator.evaluate(board))
print(evaluator.evaluate(board))
print(evaluator.evaluate(board))