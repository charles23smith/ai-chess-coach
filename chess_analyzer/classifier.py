def classify_move(uci, best_move, eval_loss):
    
    if uci == best_move:
        classification = "Best"
    elif eval_loss < 50:
        classification = "Good"
    elif eval_loss < 100:
        classification = "Inaccuracy"
    elif eval_loss < 200:
        classification = "Mistake"
    else:
        classification = "Blunder"

    return classification