# ChessAI ♟️

A Python-based chess engine featuring a graphical user interface (GUI) and an AI opponent. The AI uses the **Negamax algorithm with quiescence search**, enhanced by positional evaluation heuristics and basic tactical awareness.

## 🚀 Features

- Play against a challenging AI opponent
- Real-time GUI built with `pygame`
- AI logic using:
  - Material scoring
  - Positional piece-square tables
  - Hanging piece detection
  - Weaker attacker penalties
  - Quiescence search
- Move history log (Move_log.txt)
- "Checkmate" and game end detection

## 🧠 AI Overview

The AI is implemented in `NeaChessAI.py` and includes:
- A `Negamax` tree search with alpha-beta pruning
- Quiescence search to reduce horizon effect
- Evaluation function that blends material + positional scoring
- Bonus/malus for checks, centralization, and piece safety

## 📁 Project Structure

├── images/ # Piece images

├── NeaChessMain.py # Main GUI + game loop

├── NeaChessEngine.py # Move generation & game state

├── NeaChessAI.py # AI engine & evaluation logic

├── Move_log.txt # Output move log


## ▶️ How to Run

1. Make sure you have Python 3 installed.
2. Install dependencies:
  pip install pygame
3. Run the main game:
python NeaChessMain.py
![image](https://github.com/user-attachments/assets/435ed4fd-ddeb-4b61-b6b6-abeef27d7e6f)

## Enjoy the game and try to beat my own creation 😄





