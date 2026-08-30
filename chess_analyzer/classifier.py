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
        mate_after, 
        sacrifice_value
):

    if sacrifice_value >= 2 and eval_loss <= 50:
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

def calculate_material_loss(board, color, move_played, continuation):
    start_balance = material_balance(board, color)
    future_board = board.copy()

    if move_played not in future_board.legal_moves:
        return 0

    for move in continuation:
        if move not in future_board.legal_moves:
            break

        future_board.push(move)

    end_balance = material_balance(future_board, color)

    return max(0, start_balance - end_balance)

def calculate_sacrifice_value(board_before, move):
    moving_piece = board_before.piece_at(move.from_square)

    if moving_piece is None:
        return 0

    moving_value = PIECE_VALUES.get(moving_piece.piece_type, 0)

    captured_piece = board_before.piece_at(move.to_square)

    captured_value = 0
    if captured_piece is not None:
        captured_value = PIECE_VALUES.get(captured_piece.piece_type, 0)

    board_after = board_before.copy()
    board_after.push(move)

    sacrifice_value = max(0, moving_value - captured_value)

    if sacrifice_value == 0:
        return 0

    # Can the opponent capture the moved piece?
    capture_exists = False

    for response in board_after.legal_moves:
        if response.to_square == move.to_square:
            capture_exists = True
            break

    if not capture_exists:
        return 0

    # Check whether the moved piece is defended by the player
    moved_piece_color = moving_piece.color

    defenders = board_after.attackers(
        moved_piece_color,
        move.to_square
    )

    if defenders:
        return 0

    return sacrifice_value


def get_classification_icon(classification):
    icons = {
        "Brilliant": ("!!", "#3b82f6"),     # Blue
        "Best": ("★", "#22c55e"),           # Green
        "Good": ("✓", "#86b96b"),           # Lighter/muted green
        "Inaccuracy": ("?!", "#eab308"),     # Yellow
        "Mistake": ("?", "#f97316"),         # Orange
        "Blunder": ("??", "#ef4444")         # Red
    }

    return icons.get(classification, ("", "#777777"))