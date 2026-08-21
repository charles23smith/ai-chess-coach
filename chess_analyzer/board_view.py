import chess.svg
import streamlit as st

def display_chess_board(game_data):
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
    else:
        current_move = game_data["Moves"][st.session_state["move_index"]]
        board = chess.Board(current_move["Fen"])

    svg = chess.svg.board(board)
    st.image(svg)


def next_move(total_moves):
    if st.session_state["move_index"] < total_moves - 1:
         st.session_state["move_index"] += 1 

def previous_move():
    if st.session_state["move_index"] > -1:
        st.session_state["move_index"] -= 1 

