import functools
import random

from app.data import FREE_SPACE, QUESTIONS
from app.models import BingoLine, BingoSquareData

BOARD_SIZE = 5
CENTER_INDEX = 12  # 5x5 grid, center is index 12 (row 2, col 2)
CLASSIC_SQUARE_COUNT = BOARD_SIZE * BOARD_SIZE
CLASSIC_QUESTION_COUNT = CLASSIC_SQUARE_COUNT - 1


def generate_board() -> list[BingoSquareData]:
    """Generate a new 5x5 bingo board."""
    questions = iter(random.sample(QUESTIONS, CLASSIC_QUESTION_COUNT))
    return [
        BingoSquareData(id=i, text=FREE_SPACE, is_marked=True, is_free_space=True)
        if i == CENTER_INDEX
        else BingoSquareData(id=i, text=next(questions))
        for i in range(CLASSIC_SQUARE_COUNT)
    ]


def generate_scavenger_list() -> list[BingoSquareData]:
    """Generate a scavenger checklist using the same question pool."""
    questions = random.sample(QUESTIONS, len(QUESTIONS))
    return [BingoSquareData(id=i, text=text) for i, text in enumerate(questions)]


def generate_card_deck() -> list[str]:
    """Generate a shuffled list of question cards."""
    return random.sample(QUESTIONS, len(QUESTIONS))


def draw_card(deck: list[str]) -> tuple[str, list[str]]:
    """Draw one card from a deck. Re-shuffle when deck is empty."""
    active_deck = deck or generate_card_deck()
    return active_deck[0], active_deck[1:]


def toggle_square(
    board: list[BingoSquareData], square_id: int
) -> list[BingoSquareData]:
    """Toggle a square's marked state. Returns a new board list."""
    return [
        sq.model_copy(update={"is_marked": not sq.is_marked})
        if sq.id == square_id and not sq.is_free_space
        else sq
        for sq in board
    ]


@functools.cache
def _get_winning_lines() -> tuple[BingoLine, ...]:
    """Get all possible winning lines (cached)."""
    lines: list[BingoLine] = []

    for row in range(BOARD_SIZE):
        squares = [row * BOARD_SIZE + col for col in range(BOARD_SIZE)]
        lines.append(BingoLine(type="row", index=row, squares=squares))

    for col in range(BOARD_SIZE):
        squares = [row * BOARD_SIZE + col for row in range(BOARD_SIZE)]
        lines.append(BingoLine(type="column", index=col, squares=squares))

    lines.append(BingoLine(type="diagonal", index=0, squares=[0, 6, 12, 18, 24]))
    lines.append(BingoLine(type="diagonal", index=1, squares=[4, 8, 12, 16, 20]))

    return tuple(lines)


def check_bingo(board: list[BingoSquareData]) -> BingoLine | None:
    """Check if there's a bingo and return the winning line."""
    if len(board) < CLASSIC_SQUARE_COUNT:
        return None
    return next(
        (
            line
            for line in _get_winning_lines()
            if all(board[idx].is_marked for idx in line.squares)
        ),
        None,
    )


def is_scavenger_complete(board: list[BingoSquareData]) -> bool:
    """Scavenger mode is complete when every checklist item is marked."""
    return len(board) > 0 and all(square.is_marked for square in board)


def get_winning_square_ids(line: BingoLine | None) -> set[int]:
    """Get the square IDs that are part of a winning line."""
    return set(line.squares) if line else set()
