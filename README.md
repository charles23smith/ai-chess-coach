# AI Chess Coach ♟️

AI Chess Coach is an interactive chess analysis application built with Python and Streamlit. Users can upload PGN chess games and receive move-by-move analysis powered by the Stockfish chess engine.

The application evaluates each position, identifies the engine's best move, classifies played moves, detects tactical mistakes and sacrifices, and provides an interactive interface for reviewing the game.

## Features

### PGN Game Analysis

Upload a `.pgn` file containing a chess game and the application will automatically:

- Parse the game and reconstruct each board position
- Analyze every move using Stockfish
- Calculate the evaluation before and after each move
- Determine the Stockfish-recommended move
- Detect forced mating sequences
- Calculate evaluation and material loss
- Detect potential material sacrifices
- Classify each move

A progress bar displays the current analysis progress while Stockfish processes the game.

### Move Classification

Each move is automatically classified as one of:

- 🔵 **Brilliant**
- 🟢 **Best**
- 🟩 **Good**
- 🟡 **Inaccuracy**
- 🟠 **Mistake**
- 🔴 **Blunder**

The classification system combines Stockfish evaluation changes with additional information such as material loss, sacrifices, and mate sequences.

Classification icons are displayed directly on the chess board and can be enabled or disabled.

### Interactive Game Review

After analysis, users can navigate through the game using **Previous** and **Next** controls.

For each position, the application displays:

- The current board position
- The move played
- Move classification
- Stockfish's recommended move
- Position evaluation
- Previous move highlighting

### Evaluation Bar

A live evaluation bar displays Stockfish's assessment of the current position.

- Positive evaluations favor White
- Negative evaluations favor Black
- Forced mating sequences are displayed using mate evaluations

The evaluation bar updates as the user navigates through the game.

### Move History

The move history is displayed next to the board using standard algebraic notation.

Example:

| Move | White | Black |
| --- | --- | --- |
| 1 | e4 | e5 |
| 2 | Nf3 | Nc6 |
| 3 | Bb5 | Nf6 |

The table updates based on the current position being reviewed.

### Board Perspective

The board can be viewed from either player's perspective.

Users can switch between:

- White perspective
- Black perspective

Move highlighting and classification icons automatically adjust to the selected orientation.

### Game Statistics

At the end of the game, the application summarizes the number of:

- Brilliant moves
- Best moves
- Good moves
- Inaccuracies
- Mistakes
- Blunders

Statistics are tracked separately for White and Black.

## Tech Stack

- **Python**
- **Streamlit** — interactive user interface
- **python-chess** — PGN parsing, board representation, and chess logic
- **Stockfish** — chess engine analysis

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-chess-coach
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Stockfish

The application requires the Stockfish chess engine.

Make sure the Stockfish executable is available to the application and that the engine path in the project is configured correctly.

The current project expects the engine at approximately:

```text
bin/
└── stockfish.exe
```

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where the application can be opened in your browser.

## How to Use

1. Launch the application.
2. Upload a `.pgn` chess game.
3. Wait for Stockfish to finish analyzing the game.
4. Use **Next** and **Previous** to navigate through moves.
5. View the Stockfish evaluation and move classification for each position.
6. Use the **Board Perspective** control to flip the board.
7. Toggle classification icons on or off.
8. Review the move history next to the board.
9. Navigate to the final position to view game statistics.

## Project Structure

```text
ai-chess-coach/
│
├── app.py
│
├── bin/
│   └── stockfish.exe
│
└── chess_analyzer/
    ├── __init__.py
    ├── board_view.py
    ├── classifier.py
    ├── engine.py
    └── pgn_parser.py
```

### Main Components

**`app.py`**

Handles the Streamlit application, PGN uploads, session state, and application flow.

**`pgn_parser.py`**

Parses PGN files, reconstructs positions, sends positions to Stockfish, and creates structured game analysis data.

**`engine.py`**

Manages communication with Stockfish and retrieves evaluations, recommended moves, mating sequences, and principal variations.

**`classifier.py`**

Contains the custom move-classification logic used to identify brilliant moves, best moves, inaccuracies, mistakes, blunders, material losses, and sacrifices.

**`board_view.py`**

Handles board visualization, move navigation, evaluation display, move history, classification icons, statistics, and board orientation.

## Current Development

AI Chess Coach is actively being developed. Current development goals include:

- PostgreSQL game persistence
- REST API backend
- Previously analyzed game history
- Player performance analytics
- Personalized improvement recommendations
- What-if move analysis
- Automated testing
- UI improvements
- Deployment

## Disclaimer

Move classifications are generated using custom heuristics built on top of Stockfish analysis. Labels such as **Brilliant**, **Mistake**, and **Blunder** may therefore differ from classifications produced by other chess platforms.

## Author

**Charles Smith**

Computer Engineering  
Texas A&M University