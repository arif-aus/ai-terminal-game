import game
from unittest.mock import patch


def reset_game() -> None:
    """Reset all game state before each test."""
    game.player_pos[0] = 0
    game.player_pos[1] = 0
    game.score = 0
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1
    game.hazard_pos[0] = 4
    game.hazard_pos[1] = 4


# --- Movement Tests ---


def test_move_right() -> None:
    reset_game()
    game.move_player("d")
    assert game.player_pos == [0, 1]


def test_move_down() -> None:
    reset_game()
    game.move_player("s")
    assert game.player_pos == [1, 0]


def test_move_left_from_middle() -> None:
    reset_game()
    game.player_pos[1] = 2
    game.move_player("a")
    assert game.player_pos == [0, 1]


def test_move_up_from_middle() -> None:
    reset_game()
    game.player_pos[0] = 2
    game.move_player("w")
    assert game.player_pos == [1, 0]


def test_multiple_moves() -> None:
    reset_game()
    game.move_player("d")
    game.move_player("d")
    game.move_player("s")
    game.move_player("s")
    assert game.player_pos == [2, 2]


# --- Boundary Tests ---


def test_cannot_move_left_from_edge() -> None:
    reset_game()
    game.move_player("a")
    assert game.player_pos == [0, 0]


def test_cannot_move_up_from_edge() -> None:
    reset_game()
    game.move_player("w")
    assert game.player_pos == [0, 0]


def test_cannot_move_right_from_edge() -> None:
    reset_game()
    game.player_pos[1] = game.GRID_SIZE - 1
    game.move_player("d")
    assert game.player_pos[1] == game.GRID_SIZE - 1


def test_cannot_move_down_from_edge() -> None:
    reset_game()
    game.player_pos[0] = game.GRID_SIZE - 1
    game.move_player("s")
    assert game.player_pos[0] == game.GRID_SIZE - 1


def test_cannot_move_off_bottom_right_corner() -> None:
    reset_game()
    game.player_pos[0] = game.GRID_SIZE - 1
    game.player_pos[1] = game.GRID_SIZE - 1
    game.move_player("s")
    game.move_player("d")
    assert game.player_pos == [game.GRID_SIZE - 1, game.GRID_SIZE - 1]


# --- Grid Drawing Tests ---


def test_draw_grid_contains_player(capsys) -> None:
    reset_game()
    game.draw_grid()
    output = capsys.readouterr().out
    assert " P " in output


def test_draw_grid_contains_dots(capsys) -> None:
    reset_game()
    game.draw_grid()
    output = capsys.readouterr().out
    assert " . " in output


def test_draw_grid_contains_dividers(capsys) -> None:
    reset_game()
    game.draw_grid()
    output = capsys.readouterr().out
    assert "---" in output
    assert "|" in output


def test_draw_grid_shows_player_at_new_position(capsys) -> None:
    reset_game()
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


# --- Collectible Tests ---


def test_collectible_not_on_player() -> None:
    """Spawn should never place the collectible on the player."""
    reset_game()
    for _ in range(20):
        game.spawn_collectible()
        assert game.collectible_pos != game.player_pos


def test_spawn_collectible_within_grid() -> None:
    """Collectible should always be inside the grid bounds."""
    reset_game()
    for _ in range(20):
        game.spawn_collectible()
        assert 0 <= game.collectible_pos[0] < game.GRID_SIZE
        assert 0 <= game.collectible_pos[1] < game.GRID_SIZE


def test_draw_grid_contains_collectible(capsys) -> None:
    reset_game()
    game.draw_grid()
    output = capsys.readouterr().out
    assert " C " in output


# --- Scoring Tests ---


def test_collect_increases_score() -> None:
    reset_game()
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1  # Place collectible to the right of player
    game.move_player("d")  # Move onto collectible
    assert game.score == 1


def test_collect_respawns_collectible() -> None:
    reset_game()
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1
    old_pos = game.collectible_pos[:]
    game.move_player("d")
    # Collectible should have moved to a new position
    assert game.collectible_pos != old_pos


def test_collect_multiple_times() -> None:
    reset_game()
    for i in range(3):
        game.collectible_pos[0] = 0
        game.collectible_pos[1] = 1
        game.move_player("d")  # Collect at (0,1)
        # Move collectible far away to avoid accidental collection on return
        game.collectible_pos[0] = game.GRID_SIZE - 1
        game.collectible_pos[1] = game.GRID_SIZE - 1
        game.move_player("a")  # Move back to (0,0)
    assert game.score == 3


def test_score_displays_in_grid(capsys) -> None:
    reset_game()
    game.score = 7
    game.draw_grid()
    output = capsys.readouterr().out
    assert "7/10" in output


def test_no_score_when_missing_collectible() -> None:
    reset_game()
    game.collectible_pos[0] = 2
    game.collectible_pos[1] = 2  # Collectible far away
    game.move_player("d")  # Move to (0, 1) — not the collectible
    assert game.score == 0


# --- Hazard Tests ---


def test_hazard_not_on_player() -> None:
    """Spawn should never place the hazard on the player."""
    reset_game()
    for _ in range(20):
        game.spawn_hazard()
        assert game.hazard_pos != game.player_pos


def test_hazard_not_on_collectible() -> None:
    """Spawn should never place the hazard on the collectible."""
    reset_game()
    for _ in range(20):
        game.spawn_hazard()
        assert game.hazard_pos != game.collectible_pos


def test_spawn_hazard_within_grid() -> None:
    """Hazard should always be inside the grid bounds."""
    reset_game()
    for _ in range(20):
        game.spawn_hazard()
        assert 0 <= game.hazard_pos[0] < game.GRID_SIZE
        assert 0 <= game.hazard_pos[1] < game.GRID_SIZE


def test_draw_grid_contains_hazard(capsys) -> None:
    reset_game()
    game.draw_grid()
    output = capsys.readouterr().out
    assert " X " in output


def test_hitting_hazard_returns_true() -> None:
    reset_game()
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 1  # Hazard to the right of player
    result = game.move_player("d")
    assert result is True


def test_hazard_moves_player() -> None:
    reset_game()
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 1
    game.move_player("d")
    assert game.player_pos == [0, 1]


def test_not_hitting_hazard_returns_false() -> None:
    reset_game()
    game.hazard_pos[0] = 4
    game.hazard_pos[1] = 4  # Hazard far away
    result = game.move_player("d")
    assert result is False


def test_hazard_stops_score_increment() -> None:
    """Player should not score if they land on the hazard."""
    reset_game()
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 1
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1  # Same spot as hazard — hazard takes priority
    game.move_player("d")
    assert game.score == 0


# --- Reset Tests ---


def test_reset_game_moves_player_to_origin() -> None:
    reset_game()
    game.move_player("d")
    game.move_player("s")
    game.reset_game()
    assert game.player_pos == [0, 0]


def test_reset_game_resets_score() -> None:
    reset_game()
    game.score = 5
    game.reset_game()
    assert game.score == 0


def test_reset_game_spawns_new_collectible() -> None:
    reset_game()
    old_collectible = game.collectible_pos[:]
    # Move player to collectible, collect it, then reset
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1
    game.move_player("d")
    game.reset_game()
    # After reset, collectible should exist and not be on the player
    assert game.collectible_pos != game.player_pos


def test_reset_game_spawns_new_hazard() -> None:
    reset_game()
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 1
    game.reset_game()
    # After reset, hazard should exist and not be on the player or collectible
    assert game.hazard_pos != game.player_pos
    assert game.hazard_pos != game.collectible_pos


# --- Play Round Tests ---


def test_play_round_returns_quit() -> None:
    """Quitting during a round should return 'quit'."""
    reset_game()
    with patch("builtins.input", return_value="quit"):
        result = game.play_round()
    assert result == "quit"


def test_play_round_returns_lose_on_hazard() -> None:
    """Hitting the hazard should return 'lose'."""
    reset_game()
    game.hazard_pos[0] = 0
    game.hazard_pos[1] = 1  # Right next to player
    with patch("builtins.input", side_effect=["d"]), \
         patch.object(game, "reset_game"):
        result = game.play_round()
    assert result == "lose"


def test_play_round_returns_win_on_score() -> None:
    """Reaching WIN_SCORE should return 'win'."""
    reset_game()
    game.score = game.WIN_SCORE - 1
    game.collectible_pos[0] = 0
    game.collectible_pos[1] = 1  # Collectible next to player
    with patch("builtins.input", side_effect=["d"]), \
         patch.object(game, "reset_game"):
        result = game.play_round()
    assert result == "win"


def test_play_round_resets_state() -> None:
    """Starting a new round should reset the player to origin."""
    reset_game()
    game.player_pos[0] = 3
    game.player_pos[1] = 3
    game.score = 9
    with patch("builtins.input", return_value="quit"):
        game.play_round()
    # play_round calls reset_game at the start, so state is reset
    # (then quit returns immediately — but reset already happened)
    assert game.player_pos == [0, 0]
    assert game.score == 0
