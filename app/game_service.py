from dataclasses import dataclass, field

from app.game_logic import (
    check_bingo,
    draw_card,
    generate_board,
    generate_card_deck,
    generate_scavenger_list,
    get_winning_square_ids,
    is_scavenger_complete,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData, GameMode, GameState


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_state: GameState = GameState.START
    game_mode: GameMode = GameMode.CLASSIC
    board: list[BingoSquareData] = field(default_factory=list)
    card_deck: list[str] = field(default_factory=list)
    current_card: str | None = None
    winning_line: BingoLine | None = None
    show_bingo_modal: bool = False

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    @property
    def is_scavenger_mode(self) -> bool:
        return self.game_mode == GameMode.SCAVENGER

    @property
    def is_deck_mode(self) -> bool:
        return self.game_mode == GameMode.DECK

    @property
    def instruction_text(self) -> str:
        if self.is_scavenger_mode:
            return "Mark each prompt as you find a matching person."
        if self.is_deck_mode:
            return "Tap Draw Card to get a random player question."
        return "Tap a square when you find someone who matches it."

    @property
    def completion_banner_text(self) -> str:
        if self.is_scavenger_mode:
            return "SCAVENGER COMPLETE! You found everyone!"
        return "BINGO! You got a line!"

    @property
    def modal_title(self) -> str:
        if self.is_scavenger_mode:
            return "HUNT COMPLETE!"
        return "BINGO!"

    @property
    def modal_message(self) -> str:
        if self.is_scavenger_mode:
            return "You checked every prompt."
        return "You completed a line!"

    @property
    def checked_count(self) -> int:
        return sum(1 for square in self.board if square.is_marked)

    @property
    def total_checkable(self) -> int:
        return len(self.board)

    @property
    def progress_percent(self) -> int:
        if self.total_checkable == 0:
            return 0
        return int((self.checked_count / self.total_checkable) * 100)

    def _set_completed_state(self) -> None:
        self.game_state = GameState.BINGO
        self.show_bingo_modal = True

    def start_game(self, mode: GameMode = GameMode.CLASSIC) -> None:
        self.game_mode = mode
        if mode == GameMode.DECK:
            self.board = []
            self.card_deck = generate_card_deck()
            self.current_card = None
        else:
            board_factory = (
                generate_scavenger_list
                if mode == GameMode.SCAVENGER
                else generate_board
            )
            self.board = board_factory()
            self.card_deck = []
            self.current_card = None
        self.winning_line = None
        self.game_state = GameState.PLAYING
        self.show_bingo_modal = False

    def draw_card_for_deck_mode(self) -> None:
        if self.game_state != GameState.PLAYING or not self.is_deck_mode:
            return
        self.current_card, self.card_deck = draw_card(self.card_deck)

    def handle_square_click(self, square_id: int) -> None:
        if self.game_state != GameState.PLAYING:
            return
        self.board = toggle_square(self.board, square_id)

        if self.game_mode == GameMode.SCAVENGER:
            if is_scavenger_complete(self.board):
                self._set_completed_state()
            return

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self._set_completed_state()

    def reset_game(self) -> None:
        self.game_state = GameState.START
        self.game_mode = GameMode.CLASSIC
        self.board = []
        self.card_deck = []
        self.current_card = None
        self.winning_line = None
        self.show_bingo_modal = False

    def dismiss_modal(self) -> None:
        self.show_bingo_modal = False
        self.game_state = GameState.PLAYING


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
