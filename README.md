# Danger Game: Dragon's Den

A terminal-based adventure game where you navigate a 🧙 wizard through a dangerous 5x5 grid, collecting 💎 gems while avoiding a fierce 🐉 dragon. Built with Python as a demonstration of iterative game development and test-driven engineering.

```
=== Danger Game ===
Score: 3/10

 . | . | . | . | .
-----------------
 . | 🧙 | . | . | .
-----------------
 . | . | . | 💎 | .
-----------------
 . | . | . | . | .
-----------------
 . | 🐉 | . | . | .
```

## Features

- **WASD Movement** — Navigate the grid with `W` (up), `A` (left), `S` (down), and `D` (right). Boundary checks prevent moving off the grid.
- **Collectible System** — 💎 gems spawn at random positions. Collect 10 to win.
- **Hazard System** — A 🐉 dragon sits on a random tile. Step on it and the game ends.
- **Win/Lose Conditions** — Reach a score of 10 for "Winner", or hit the dragon for "Try next time".
- **Play Again** — After each round, choose to play again or exit cleanly.
- **Themed Interface** — Custom emojis, story intro, and game name displayed at startup.
- **Automated Tests** — 38 pytest tests covering movement, boundaries, collectibles, hazards, scoring, game reset, and round flow.

## How to Run

### Prerequisites

- Python 3.10 or higher
- pytest (for running tests)

### Launch the Game

```bash
python game.py
```

### Run the Tests

```bash
python -m pytest test_game.py -v
```

## How to Play

| Key | Action |
|-----|--------|
| `W` | Move up |
| `A` | Move left |
| `S` | Move down |
| `D` | Move right |
| `quit` | Exit the game |

Collect 💎 gems to increase your score. Avoid the 🐉 dragon at all costs. Reach a score of 10 to win!

## What I Learned

- **Iterative Development** — The game was built layer by layer: first a static grid, then movement, then collectibles, hazards, scoring, play again, and finally theming. Each iteration was tested before moving to the next, making it easy to isolate and fix issues early.

- **Engineering Prompts to Prevent Regression** — Every time a new feature was added, existing tests were run first to catch unintended side effects. For example, adding the emoji theme broke 4 grid-drawing tests that were checking for old ASCII characters (`P`, `C`, `X`). Updating those tests to use theme constants (`PLAYER_EMOJI`, `COLLECTIBLE_EMOJI`, `HAZARD_EMOJI`) ensured the tests would stay valid if the emojis were ever changed.

- **Automated Testing with pytest** — Writing tests alongside features turned out to be one of the most valuable practices. Tests caught real bugs — like a missing `global score` declaration in `reset_game()` that silently created a local variable instead of resetting the actual game score. Using `unittest.mock` to mock `input()` and control game state made it possible to test interactive functions like `play_round()` without needing a real terminal session.

## Project Structure

```
ai-terminal-game/
├── game.py          # Main game logic and entry point
├── test_game.py     # 38 pytest tests
└── README.md        # This file
```

## License

This project was built as a learning exercise by Correlation One.
