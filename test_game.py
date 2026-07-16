import game


def reset_player() -> None:
    """Reset player position to origin before each test."""
    game.player_pos[0] = 0
    game.player_pos[1] = 0


# --- Movement Tests ---


def test_move_right() -> None:
    reset_player()
    game.move_player("d")
    assert game.player_pos == [0, 1]


def test_move_down() -> None:
    reset_player()
    game.move_player("s")
    assert game.player_pos == [1, 0]


def test_move_left_from_middle() -> None:
    reset_player()
    game.player_pos[1] = 2
    game.move_player("a")
    assert game.player_pos == [0, 1]


def test_move_up_from_middle() -> None:
    reset_player()
    game.player_pos[0] = 2
    game.move_player("w")
    assert game.player_pos == [1, 0]


def test_multiple_moves() -> None:
    reset_player()
    game.move_player("d")
    game.move_player("d")
    game.move_player("s")
    game.move_player("s")
    assert game.player_pos == [2, 2]


# --- Boundary Tests ---


def test_cannot_move_left_from_edge() -> None:
    reset_player()
    game.move_player("a")
    assert game.player_pos == [0, 0]


def test_cannot_move_up_from_edge() -> None:
    reset_player()
    game.move_player("w")
    assert game.player_pos == [0, 0]


def test_cannot_move_right_from_edge() -> None:
    reset_player()
    game.player_pos[1] = game.GRID_SIZE - 1
    game.move_player("d")
    assert game.player_pos[1] == game.GRID_SIZE - 1


def test_cannot_move_down_from_edge() -> None:
    reset_player()
    game.player_pos[0] = game.GRID_SIZE - 1
    game.move_player("s")
    assert game.player_pos[0] == game.GRID_SIZE - 1


def test_cannot_move_off_bottom_right_corner() -> None:
    reset_player()
    game.player_pos[0] = game.GRID_SIZE - 1
    game.player_pos[1] = game.GRID_SIZE - 1
    game.move_player("s")
    game.move_player("d")
    assert game.player_pos == [game.GRID_SIZE - 1, game.GRID_SIZE - 1]


# --- Grid Drawing Tests ---


def test_draw_grid_contains_player(capsys) -> None:
    reset_player()
    game.draw_grid()
    output = capsys.readouterr().out
    assert " P " in output


def test_draw_grid_contains_dots(capsys) -> None:
    reset_player()
    game.draw_grid()
    output = capsys.readouterr().out
    assert " . " in output


def test_draw_grid_contains_dividers(capsys) -> None:
    reset_player()
    game.draw_grid()
    output = capsys.readouterr().out
    assert "---" in output
    assert "|" in output


def test_draw_grid_shows_player_at_new_position(capsys) -> None:
    reset_player()
    game.move_player("d")
    game.move_player("s")
    game.draw_grid()
    output = capsys.readouterr().out
    # Player should now be at (1, 1) — check the second row contains P
    lines = output.strip().split("\n")
    # The grid rows start after the header lines
    grid_rows = [line for line in lines if "|" in line or (" P " in line or " . " in line)]
    assert len(grid_rows) == game.GRID_SIZE
    # Row 1 (index 1) should contain the player
    assert " P " in grid_rows[1]
