from urllib.error import URLError

import pytest

from app.core.card import CardDraft
from app.integrations.anki.ankiconnect_client import (
    DEFAULT_DECK,
    DEFAULT_NOTE_TYPE,
    AnkiConnectClient,
    AnkiConnectError,
)


def _card() -> CardDraft:
    return CardDraft(
        expression="冒険",
        reading="ぼうけん",
        meaning="adventure",
        sentence="これから ぼうけんが はじまる！",
        source="Pokemon",
        tags="pokemon vocab",
    )


def test_build_add_note_payload_uses_fixed_v1_mapping() -> None:
    payload = AnkiConnectClient().build_add_note_payload(_card())
    note = payload["params"]["note"]

    assert payload["action"] == "addNote"
    assert payload["version"] == 6
    assert note["deckName"] == DEFAULT_DECK
    assert note["modelName"] == DEFAULT_NOTE_TYPE
    assert note["fields"] == {
        "Expression": "冒険",
        "Reading": "ぼうけん",
        "Meaning": "adventure",
        "Sentence": "これから ぼうけんが はじまる！",
        "Source": "Pokemon",
        "Tags": "pokemon vocab",
    }
    assert note["options"]["allowDuplicate"] is False
    assert note["tags"] == ["pokemon", "vocab"]


def test_add_card_successful_response_returns_note_id() -> None:
    client = AnkiConnectClient()
    client._request = lambda payload: {"result": 12345, "error": None}

    assert client.add_card(_card()) == 12345


def test_add_card_error_response_raises_ankiconnect_error() -> None:
    client = AnkiConnectClient()
    client._request = lambda payload: {"result": None, "error": "duplicate"}

    with pytest.raises(AnkiConnectError, match="duplicate"):
        client.add_card(_card())


def test_add_card_unexpected_response_raises_ankiconnect_error() -> None:
    client = AnkiConnectClient()
    client._request = lambda payload: {"result": "not-an-int", "error": None}

    with pytest.raises(AnkiConnectError, match="unexpected"):
        client.add_card(_card())


def test_request_network_failure_raises_ankiconnect_error(monkeypatch) -> None:
    def fail_urlopen(request, timeout):
        raise URLError("offline")

    monkeypatch.setattr("app.integrations.anki.ankiconnect_client.urlopen", fail_urlopen)

    with pytest.raises(AnkiConnectError, match="Could not reach AnkiConnect"):
        AnkiConnectClient()._request({"action": "version"})
