import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from app.core.card import CardDraft


ANKI_CONNECT_URL = "http://127.0.0.1:8765"
ANKI_CONNECT_VERSION = 6
DEFAULT_DECK = "Japanese Mining"
DEFAULT_NOTE_TYPE = "JP Vocab"


class AnkiConnectError(RuntimeError):
    pass


class AnkiConnectClient:
    def __init__(self, endpoint: str = ANKI_CONNECT_URL, timeout: float = 10.0) -> None:
        self.endpoint = endpoint
        self.timeout = timeout

    def add_card(self, card: CardDraft) -> int:
        payload = self.build_add_note_payload(card)
        response = self._request(payload)

        if response.get("error"):
            raise AnkiConnectError(str(response["error"]))

        note_id = response.get("result")
        if not isinstance(note_id, int):
            raise AnkiConnectError("AnkiConnect returned an unexpected response.")

        return note_id

    def build_add_note_payload(self, card: CardDraft) -> dict:
        return {
            "action": "addNote",
            "version": ANKI_CONNECT_VERSION,
            "params": {
                "note": {
                    "deckName": DEFAULT_DECK,
                    "modelName": DEFAULT_NOTE_TYPE,
                    "fields": card.to_anki_fields(),
                    "options": {
                        "allowDuplicate": False,
                    },
                    "tags": card.parsed_tags(),
                }
            },
        }

    def _request(self, payload: dict) -> dict:
        request_body = json.dumps(payload).encode("utf-8")
        request = Request(
            self.endpoint,
            data=request_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                response_body = response.read().decode("utf-8")
        except (OSError, URLError) as exc:
            raise AnkiConnectError(
                "Could not reach AnkiConnect. Make sure Anki is running and the AnkiConnect add-on is installed."
            ) from exc

        try:
            parsed_response = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise AnkiConnectError("AnkiConnect returned invalid JSON.") from exc

        if not isinstance(parsed_response, dict):
            raise AnkiConnectError("AnkiConnect returned an unexpected response.")

        return parsed_response
