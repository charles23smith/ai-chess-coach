from chess_analyzer.pgn_parser import parse_pgn
from chess_analyzer.board_view import display_chess_board
import streamlit as st 
import io

st.title("AI-Chess-App")

uploaded_games = st.file_uploader(
    "Choose PGN file", 
    type=["pgn"], 
    accept_multiple_files=True
)

if uploaded_games:
    for uploaded_game in uploaded_games:
        st.write(uploaded_game.name)

        if "game_data" not in st.session_state:
            pgn_text = uploaded_game.getvalue().decode("utf-8")
            pgn_file = io.StringIO(pgn_text)

            st.session_state["game_data"] = parse_pgn(pgn_file)
            st.session_state["move_index"] = -1

        display_chess_board(st.session_state["game_data"])
        

        