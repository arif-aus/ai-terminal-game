import os
import random

# Game constants
GRID_SIZE = 5
WIN_SCORE = 10

# Game state
player_pos = [0, 0]
score = 0
collectible_pos = [0, 0]
hazard_pos = [0, 0]


def reset_game() -> None:
    """Reset all game state for a new game."""
    global score
    player_pos[0] = 0
    player_pos[1] = 0
    score = 0
    spawn_collectible()
    spawn_hazard()


def spawn_collectible() -> None:
    """Place the collectible at a random position that isn't the player."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if [row, col] != player_pos:
            collectible_pos[0] = row
            collectible_pos[1] = col
            break


def spawn_hazard() -> None:
    """Place the hazard at a random position that isn't the player or collectible."""
    while True:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if [row, col] != player_pos and [row, col] != collectible_pos:
            hazard_pos[0] = row
            hazard_pos[1] = col
            break


def draw_grid() -> None:
    """Draw the 5x5 grid with all game elements."""
    os.system("clear" if os.name != "nt" else "cls")

    print("=== Text Adventure ===")
    print(f"Score: {score}/{WIN_SCORE}")
    print("Type 'quit' to exit.\n")

    for row in range(GRID_SIZE):
        row_display = ""
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                row_display += " P "
            elif row == collectible_pos[0] and col == collectible_pos[1]:
                row_display += " C "
            elif row == hazard_pos[0] and col == hazard_pos[1]:
                row_display += " X "
            else:
                row_display += " . "
            if col < GRID_SIZE - 1:
                row_display += "|"
        print(row_display)
        if row < GRID_SIZE - 1:
            print("---" * GRID_SIZE + "--")

    print()


def move_player(direction: str) -> bool:
    """Move the player in the given direction if within bounds.
    Returns True if the player hit the hazard."""
    row, col = player_pos[0], player_pos[1]

    if direction == "w":
        row -= 1
    elif direction == "s":
        row += 1
    elif direction == "a":
        col -= 1
    elif direction == "d":
        col += 1

    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        player_pos[0] = row
        player_pos[1] = col

        if player_pos[0] == hazard_pos[0] and player_pos[1] == hazard_pos[1]:
            return True

        if player_pos[0] == collectible_pos[0] and player_pos[1] == collectible_pos[1]:
            global score
            score += 1
            spawn_collectible()

    return False


def play_round() -> str:
    """Run a single round of the game. Returns 'win', 'lose', or 'quit'."""
    reset_game()

    while True:
        draw_grid()
        user_input = input("Command (W/A/S/D to move, 'quit' to exit): ").strip().lower()

        if user_input == "quit":
            return "quit"
        elif user_input in ["w", "a", "s", "d"]:
            hit_hazard = move_player(user_input)
            if hit_hazard:
                draw_grid()
                print("Game Over!")
                return "lose"
            if score >= WIN_SCORE:
                draw_grid()
                print(f"You collected {WIN_SCORE} items! You win!")
                return "win"
        else:
            print(f"Unknown command: '{user_input}'. Use W/A/S/D to move.")
            input("Press Enter to continue...")


def main() -> None:
    """Main game loop with play again support."""
    print("Welcome to the Grid Game!")
    print("You are 'P'. Collect 'C' items to score!")
    print(f"Collect {WIN_SCORE} items to win! Avoid the 'X' hazard!\n")
    input("Press Enter to start...")

    while True:
        result = play_round()

        if result == "quit":
            print("Thanks for playing! See ya later!")
            break

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != "y":
            print("Thanks for playing! See ya later!")
            break


if __name__ == "__main__":
    main()
