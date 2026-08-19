from chess_analyzer.pgn_parser import parse_pgn
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

        pgn_text = uploaded_game.getvalue().decode("utf-8")
        pgn_file = io.StringIO(pgn_text)
        pgn = parse_pgn(pgn_file)

        st.write(pgn["White"])