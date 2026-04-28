from app.core.tokenization import KanjiCandidate, Token, TokenizationService


class FakeDictionaryClient:
    def __init__(self, known_readings: set[str]) -> None:
        self.known_readings = known_readings
        self.last_error = None

    def lookup_by_reading(self, reading: str, limit: int = 5) -> list[KanjiCandidate]:
        if reading not in self.known_readings:
            return []

        return [
            KanjiCandidate(
                expression=f"{reading}-candidate",
                reading=reading,
                meanings=("meaning",),
                is_common=False,
                source_url="https://jisho.org",
                score=1,
            )
        ][:limit]


def test_tokenize_reviewed_sentence_into_expected_tokens() -> None:
    service = TokenizationService(
        FakeDictionaryClient({"これから", "ぼうけん", "はじまる"})
    )

    tokens = service.tokenize("これから ぼうけんが はじまる！")

    assert [token.surface for token in tokens] == ["これから", "ぼうけん", "が", "はじまる"]


def test_tokenize_respects_user_spaces() -> None:
    service = TokenizationService(FakeDictionaryClient({"これから", "ぼうけん"}))

    tokens = service.tokenize("これから ぼうけん")

    assert [token.surface for token in tokens] == ["これから", "ぼうけん"]


def test_tokenize_splits_particle_from_adjacent_kana() -> None:
    service = TokenizationService(FakeDictionaryClient({"ぼうけん"}))

    tokens = service.tokenize("ぼうけんが")

    assert [token.surface for token in tokens] == ["ぼうけん", "が"]


def test_tokenize_unknown_kana_falls_back_without_crashing() -> None:
    service = TokenizationService(FakeDictionaryClient(set()))

    tokens = service.tokenize("ふにゃら")

    assert [token.surface for token in tokens] == ["ふにゃら"]


def test_get_candidates_uses_dictionary_client() -> None:
    service = TokenizationService(FakeDictionaryClient({"ぼうけん"}))

    candidates = service.get_candidates(Token("ぼうけん", 0, 4))

    assert [candidate.reading for candidate in candidates] == ["ぼうけん"]
