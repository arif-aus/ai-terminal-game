import os

# Player starting position (row, col)
player_pos = [0, 0]

GRID_SIZE = 5


def draw_grid() -> None:
    """Draw the 5x5 grid with the player position."""
    # Clear the terminal for a cleaner look
    os.system("clear" if os.name != "nt" else "cls")

    print("=== Text Adventure ===")
    print("Type 'quit' to exit.\n")

    for row in range(GRID_SIZE):
        # Print each row of the grid
        row_display = ""
        for col in range(GRID_SIZE):
            if row == player_pos[0] and col == player_pos[1]:
                row_display += " P "  # Player position
            else:
                row_display += " . "  # Empty cell
            if col < GRID_SIZE - 1:
                row_display += "|"
        print(row_display)
        # Print horizontal divider between rows (but not after the last one)
        if row < GRID_SIZE - 1:
            print("---" * GRID_SIZE + "--")

    print()


def move_player(direction: str) -> None:
    """Move the player in the given direction if within bounds."""
    row, col = player_pos[0], player_pos[1]

    if direction == "w":
        row -= 1  # Up
    elif direction == "s":
        row += 1  # Down
    elif direction == "a":
        col -= 1  # Left
    elif direction == "d":
        col += 1  # Right

    # Only move if the new position is inside the grid
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        player_pos[0] = row
        player_pos[1] = col


def main() -> None:
    """Main game loop."""
    print("Welcome to the Grid Game!")
    print("You are 'P' on a 5x5 grid.")
    print("Starting at position (0, 0).\n")

    while True:
        draw_grid()
        user_input = input("Command (W/A/S/D to move, 'quit' to exit): ").strip().lower()

        if user_input == "quit":
            print("Thanks for playing! See ya later!")
            break
        elif user_input in ["w", "a", "s", "d"]:
            move_player(user_input)
        else:
            print(f"Unknown command: '{user_input}'. Use W/A/S/D to move.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
