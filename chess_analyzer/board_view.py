import chess.svg
import streamlit as st
import math
import textwrap

def eval_to_white_percent(eval_score):
     return 100 / (1 + math.exp(-eval_score / 400))


def display_chess_board(game_data):
    #Previous and Next Move buttons
    col1, col2 = st.columns(2)
    with col1:
            if st.button(
                ("<- Previous"), 
                disabled=st.session_state["move_index"] == -1 
            ):
                previous_move()
    
    with col2:
            if st.button(
                ("Next ->"), 
                disabled=st.session_state["move_index"] == len(game_data["Moves"]) - 1
            ):
                next_move(len(game_data["Moves"]))

    if st.session_state["move_index"] == -1:
        board = chess.Board()
        eval_score = game_data["Moves"][0]["EvalBefore"]
        mate_in = game_data["Moves"][0]["MateAfter"]
        fill = {}
    else:
        current_move = game_data["Moves"][st.session_state["move_index"]]
        board = chess.Board(current_move["Fen"])
        eval_score = current_move["EvalAfter"]
        mate_in = current_move["MateAfter"]
        
        #highlight squares to show moves
        current_move = game_data["Moves"][st.session_state["move_index"]]
        uci = current_move["Uci"]
        from_square = chess.parse_square(uci[:2])
        to_square = chess.parse_square(uci[2:4])
        
        fill = {
                from_square: "#1d809999", 
                to_square: "#1d809999"
        }

    #Evaluation bar
    if mate_in is not None:
        if mate_in > 0:
            white_percent = 100
            eval_display = f'M{mate_in}'
        else:
            white_percent = 0 
            eval_display = f'M{abs(mate_in)}'
    else:
        white_percent = eval_to_white_percent(eval_score)
        eval_display = f'{eval_score / 100:+.2f}'

    black_percent = 100 - white_percent 
    eval_col, board_col = st.columns([1,8])
    
    with eval_col:
    
        bar_html = textwrap.dedent(f"""
        <div style="
            height: 500px;
            width: 45px;
            border: 1px solid gray;
            display: flex;
            flex-direction: column;
        ">
            <div style="
                height: {black_percent}%;
                background-color: #333;
            "></div>
            <div style="
                height: {white_percent}%;
                background-color: #eee;
            "></div>
        </div>
        <div style="text-align:center;">
            {eval_display}
        </div>
        """)

        st.html(bar_html)
    

    #display board, show current anaylsis of moves, and final stats
    svg = chess.svg.board(board, fill = fill)
    with board_col:
         st.image(svg)

    print_current_analysis(game_data)

    
    if st.session_state["move_index"] == len(game_data["Moves"]) - 1:
        display_final_stats(game_data)


def next_move(total_moves):
    if st.session_state["move_index"] < total_moves - 1:
         st.session_state["move_index"] += 1 

def previous_move():
    if st.session_state["move_index"] > -1:
        st.session_state["move_index"] -= 1 

def print_current_analysis(game_data):
    if st.session_state["move_index"] == -1:
          st.write("Starting position")
          return

    current_move = game_data["Moves"][st.session_state["move_index"]]

    st.write(f'Move: {current_move["Move"]} {current_move["Color"]}')
    st.write(f'Played: {current_move["San"]}')
    st.write(f'Classification: {current_move["Classification"]}')
    st.write(f'Stockfish Best Move: {current_move["BestMove"]}')

def display_final_stats(game_data):
    st.subheader("Game Summary")

    selected_color = st.segmented_control(
          "Player", 
          ["White", "Black"], 
          default= "White"
    )

    stats = game_data["Stats"][selected_color]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Brilliant", stats["Brilliant"])
    col1.metric("Best", stats["BestCount"])
    col1.metric("Good", stats["GoodCount"])
    col1.metric("Inaccuracies", stats["Inaccuracies"])
    col1.metric("Mistakes", stats["Mistakes"])
    col1.metric("Blunders", stats["Blunders"])