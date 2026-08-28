import chess

PIECE_VALUES = {
    chess.PAWN: 1, 
    chess.KNIGHT: 3, 
    chess.BISHOP: 3, 
    chess.ROOK: 5, 
    chess.QUEEN: 9
}

def classify_move(
        uci, 
        best_move, 
        eval_loss, 
        material_loss, 
        mate_before, 
        mate_after
):

    if material_loss >= 3 and eval_loss <= 50:
        return "Brilliant"
    
    if uci == best_move:
        return "Best"

    elif mate_after is not None:
        if mate_before is None and eval_loss >= 200:
            return "Blunder"

    elif eval_loss >= 200 and material_loss >= 3:
        return "Blunder"

    elif eval_loss >= 100 and material_loss >= 1:
        return "Mistake"

    elif eval_loss >= 75:
        return "Inaccuracy"

    else:
        return "Good"


def material_score(board, color):
    total = 0

    for piece_type, value in PIECE_VALUES.items():
        total += len(board.pieces(piece_type, color)) * value

    return total 

def material_balance(board, color):
    my_material = material_score(board, color)
    opponent_material = material_score(board, not color)

    return my_material - opponent_material

def calculate_material_loss(board, color, continuation):
    start_balance = material_balance(board, color)
    future_board = board.copy()

    for move in continuation:
        if move not in future_board.legal_moves:
            break

        future_board.push(move)

    end_balance = material_balance(future_board, color)

    return max(0, start_balance - end_balance)