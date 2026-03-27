import pytest
from fastapi.testclient import TestClient

from app.data import QUESTIONS
from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestHomePage:
    def test_home_returns_200(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_start_screen(self, client: TestClient) -> None:
        response = client.get("/")
        assert "Tech Life" in response.text
        assert "Start Game" in response.text
        assert "How to play" in response.text

    def test_home_sets_session_cookie(self, client: TestClient) -> None:
        response = client.get("/")
        assert "session" in response.cookies


class TestStartGame:
    def test_start_returns_game_board(self, client: TestClient) -> None:
        # First visit to get session
        client.get("/")
        response = client.post("/start")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "← Back" in response.text

    def test_board_has_25_squares(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/start")
        # Count the toggle buttons (squares with hx-post="/toggle/")
        assert response.text.count('hx-post="/toggle/') == 24  # 24 + 1 free space

    def test_scavenger_mode_returns_checklist(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/start?mode=scavenger")
        assert response.status_code == 200
        assert "Scavenger progress" in response.text
        assert "0/24" in response.text
        assert "FREE SPACE" not in response.text
        assert response.text.count('hx-post="/toggle/') == 24

    def test_deck_mode_returns_draw_card_screen(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/start?mode=deck")

        assert response.status_code == 200
        assert "Card Deck Shuffle" in response.text
        assert "Draw Card" in response.text
        assert 'hx-post="/draw-card"' in response.text


class TestToggleSquare:
    def test_toggle_marks_square(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # The response should contain the game screen with a marked square
        assert "FREE SPACE" in response.text


class TestResetGame:
    def test_reset_returns_start_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/reset")
        assert response.status_code == 200
        assert "Start Game" in response.text
        assert "How to play" in response.text


class TestDismissModal:
    def test_dismiss_returns_game_screen(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start")
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text


class TestScavengerCheckboxInputs:
    def test_scavenger_renders_real_checkbox_inputs(self, client: TestClient) -> None:
        client.get("/")
        response = client.post("/start?mode=scavenger")

        assert response.status_code == 200
        assert response.text.count('type="checkbox"') == 24

    def test_toggling_scavenger_item_checks_checkbox(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start?mode=scavenger")

        response = client.post("/toggle/0")

        assert response.status_code == 200
        assert 'type="checkbox"' in response.text
        assert 'type="checkbox" checked' in response.text


class TestDeckMode:
    def test_draw_card_reveals_question(self, client: TestClient) -> None:
        client.get("/")
        client.post("/start?mode=deck")

        response = client.post("/draw-card")

        assert response.status_code == 200
        assert "Current Card" in response.text
        assert any(question in response.text for question in QUESTIONS)
