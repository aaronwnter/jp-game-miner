from urllib.error import URLError

from app.integrations.dictionary.jisho_client import JishoDictionaryClient


def test_parse_candidates_filters_by_exact_reading_and_ranks_common_kanji() -> None:
    client = JishoDictionaryClient()
    payload = {
        "data": [
            {
                "is_common": False,
                "japanese": [{"word": "望見", "reading": "ぼうけん"}],
                "senses": [{"english_definitions": ["viewing from afar"]}],
            },
            {
                "is_common": True,
                "japanese": [{"word": "冒険", "reading": "ぼうけん"}],
                "senses": [{"english_definitions": ["adventure"]}],
            },
            {
                "is_common": True,
                "japanese": [{"word": "暴言", "reading": "ぼうげん"}],
                "senses": [{"english_definitions": ["abusive language"]}],
            },
        ]
    }

    candidates = client._parse_candidates(payload, "ぼうけん")
    candidates.sort(key=lambda candidate: (-candidate.score, len(candidate.expression)))

    assert [candidate.expression for candidate in candidates] == ["冒険", "望見"]
    assert candidates[0].meanings == ("adventure",)


def test_lookup_by_reading_limits_results() -> None:
    client = JishoDictionaryClient()
    client._fetch = lambda reading: {
        "data": [
            {
                "is_common": False,
                "japanese": [{"word": f"候補{index}", "reading": "こうほ"}],
                "senses": [{"english_definitions": [f"candidate {index}"]}],
            }
            for index in range(8)
        ]
    }

    candidates = client.lookup_by_reading("こうほ", limit=5)

    assert len(candidates) == 5


def test_lookup_by_reading_handles_network_failure() -> None:
    client = JishoDictionaryClient()

    def fail_fetch(reading: str) -> dict:
        raise URLError("offline")

    client._fetch = fail_fetch

    assert client.lookup_by_reading("ぼうけん") == []
    assert client.last_error is not None
