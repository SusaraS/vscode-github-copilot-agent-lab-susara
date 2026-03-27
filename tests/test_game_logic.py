from app.data import FREE_SPACE, QUESTIONS
from app.game_logic import (
    CENTER_INDEX,
    check_bingo,
    draw_card,
    generate_board,
    generate_card_deck,
    generate_scavenger_list,
    get_winning_square_ids,
    is_scavenger_complete,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData


class TestGenerateBoard:
    def test_board_has_25_squares(self) -> None:
        board = generate_board()
        assert len(board) == 25

    def test_center_is_free_space(self) -> None:
        board = generate_board()
        center = board[CENTER_INDEX]
        assert center.is_free_space is True
        assert center.is_marked is True
        assert center.text == FREE_SPACE

    def test_non_center_squares_are_not_free_space(self) -> None:
        board = generate_board()
        for i, square in enumerate(board):
            if i != CENTER_INDEX:
                assert square.is_free_space is False
                assert square.is_marked is False

    def test_all_questions_from_pool(self) -> None:
        board = generate_board()
        texts = {s.text for s in board if not s.is_free_space}
        assert texts.issubset(set(QUESTIONS))

    def test_squares_have_sequential_ids(self) -> None:
        board = generate_board()
        for i, square in enumerate(board):
            assert square.id == i

    def test_board_is_shuffled(self) -> None:
        """Verify two boards aren't identical (high probability)."""
        board1 = generate_board()
        board2 = generate_board()
        texts1 = [s.text for s in board1]
        texts2 = [s.text for s in board2]
        # Extremely unlikely to be identical
        assert texts1 != texts2


class TestToggleSquare:
    def test_toggle_marks_unmarked_square(self) -> None:
        board = generate_board()
        square_id = 0
        assert board[square_id].is_marked is False
        new_board = toggle_square(board, square_id)
        assert new_board[square_id].is_marked is True

    def test_toggle_unmarks_marked_square(self) -> None:
        board = generate_board()
        board = toggle_square(board, 0)
        assert board[0].is_marked is True
        board = toggle_square(board, 0)
        assert board[0].is_marked is False

    def test_toggle_does_not_affect_free_space(self) -> None:
        board = generate_board()
        new_board = toggle_square(board, CENTER_INDEX)
        assert new_board[CENTER_INDEX].is_marked is True  # Still marked

    def test_toggle_returns_new_list(self) -> None:
        board = generate_board()
        new_board = toggle_square(board, 0)
        assert board is not new_board


class TestCheckBingo:
    def _make_board(self, marked_ids: set[int]) -> list[BingoSquareData]:
        board = generate_board()
        result = []
        for square in board:
            if square.id in marked_ids or square.is_free_space:
                result.append(
                    BingoSquareData(
                        id=square.id,
                        text=square.text,
                        is_marked=True,
                        is_free_space=square.is_free_space,
                    )
                )
            else:
                result.append(square)
        return result

    def test_no_bingo_initially(self) -> None:
        board = generate_board()
        assert check_bingo(board) is None

    def test_row_bingo(self) -> None:
        # Mark first row: indices 0-4
        board = self._make_board({0, 1, 2, 3, 4})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "row"
        assert result.squares == [0, 1, 2, 3, 4]

    def test_column_bingo(self) -> None:
        # Mark first column: indices 0, 5, 10, 15, 20
        board = self._make_board({0, 5, 10, 15, 20})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "column"
        assert result.squares == [0, 5, 10, 15, 20]

    def test_diagonal_bingo(self) -> None:
        # Mark diagonal: 0, 6, 12, 18, 24 (12 is free space)
        board = self._make_board({0, 6, 18, 24})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "diagonal"
        assert result.squares == [0, 6, 12, 18, 24]

    def test_partial_line_no_bingo(self) -> None:
        board = self._make_board({0, 1, 2, 3})  # Only 4 of 5 in first row
        assert check_bingo(board) is None


class TestGetWinningSquareIds:
    def test_none_line_returns_empty_set(self) -> None:
        assert get_winning_square_ids(None) == set()

    def test_returns_square_ids(self) -> None:
        line = BingoLine(type="row", index=0, squares=[0, 1, 2, 3, 4])
        assert get_winning_square_ids(line) == {0, 1, 2, 3, 4}


class TestScavengerLogic:
    def test_scavenger_list_has_all_questions(self) -> None:
        board = generate_scavenger_list()
        assert len(board) == len(QUESTIONS)
        texts = {square.text for square in board}
        assert texts == set(QUESTIONS)

    def test_scavenger_items_start_unmarked(self) -> None:
        board = generate_scavenger_list()
        assert all(not square.is_marked for square in board)

    def test_scavenger_items_are_not_free_spaces(self) -> None:
        board = generate_scavenger_list()
        assert all(not square.is_free_space for square in board)

    def test_scavenger_completion_requires_all_marked(self) -> None:
        board = generate_scavenger_list()
        assert is_scavenger_complete(board) is False

        partially_marked = toggle_square(board, 0)
        assert is_scavenger_complete(partially_marked) is False

        completed = partially_marked
        for square in board[1:]:
            completed = toggle_square(completed, square.id)

        assert is_scavenger_complete(completed) is True


class TestDeckLogic:
    def test_generate_card_deck_contains_all_questions(self) -> None:
        deck = generate_card_deck()
        assert len(deck) == len(QUESTIONS)
        assert set(deck) == set(QUESTIONS)

    def test_draw_card_consumes_from_existing_deck(self) -> None:
        card, remaining = draw_card(["a", "b", "c"])
        assert card == "a"
        assert remaining == ["b", "c"]

    def test_draw_card_reshuffles_when_empty(self) -> None:
        card, remaining = draw_card([])
        assert card in QUESTIONS
        assert len(remaining) == len(QUESTIONS) - 1
