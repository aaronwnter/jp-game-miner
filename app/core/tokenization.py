from dataclasses import dataclass
from typing import Protocol

from app.core.text_normalizer import normalize_for_tokenization


PARTICLES = {"が", "は", "を", "に", "で", "と", "の", "へ", "も", "か"}
PUNCTUATION = set("、。！？!?「」（）『』・…")


@dataclass(frozen=True)
class Token:
    surface: str
    start: int
    end: int
    selectable: bool = True


@dataclass(frozen=True)
class KanjiCandidate:
    expression: str
    reading: str
    meanings: tuple[str, ...]
    is_common: bool
    source_url: str
    score: int


class DictionaryClient(Protocol):
    last_error: str | None

    def lookup_by_reading(self, reading: str, limit: int = 5) -> list[KanjiCandidate]:
        ...


class TokenizationService:
    def __init__(self, dictionary_client: DictionaryClient) -> None:
        self.dictionary_client = dictionary_client
        self._lookup_cache: dict[str, list[KanjiCandidate]] = {}
        self.last_error: str | None = None

    def tokenize(self, sentence: str) -> list[Token]:
        self.last_error = None

        tokens: list[Token] = []
        run_start: int | None = None
        run_chars: list[str] = []

        def flush_run() -> None:
            nonlocal run_start, run_chars
            if run_start is None or not run_chars:
                run_start = None
                run_chars = []
                return

            tokens.extend(self._tokenize_hiragana_run("".join(run_chars), run_start))
            run_start = None
            run_chars = []

        for index, char in enumerate(sentence):
            if char.isspace() or char in PUNCTUATION:
                flush_run()
                continue

            if _is_hiragana(char):
                if run_start is None:
                    run_start = index
                run_chars.append(char)
                continue

            flush_run()
            tokens.append(Token(surface=char, start=index, end=index + 1, selectable=True))

        flush_run()

        return [token for token in tokens if normalize_for_tokenization(token.surface)]

    def get_candidates(self, token: Token) -> list[KanjiCandidate]:
        self.last_error = None
        candidates = self._lookup(token.surface, limit=5)
        self.last_error = getattr(self.dictionary_client, "last_error", None)
        return candidates[:5]

    def _tokenize_hiragana_run(self, text: str, start: int) -> list[Token]:
        if not text:
            return []

        tokens: list[Token] = []
        index = 0

        while index < len(text):
            particle = self._particle_at(text, index)
            if particle:
                tokens.append(Token(surface=particle, start=start + index, end=start + index + 1))
                index += 1
                continue

            match = self._longest_dictionary_match(text, index)
            if match:
                tokens.append(Token(surface=match, start=start + index, end=start + index + len(match)))
                index += len(match)
                continue

            unknown = text[index:]
            tokens.append(Token(surface=unknown, start=start + index, end=start + index + len(unknown)))
            index += len(unknown)

        return tokens

    def _longest_dictionary_match(self, text: str, index: int) -> str | None:
        for end in range(len(text), index, -1):
            candidate = text[index:end]
            if len(candidate) == 1 and candidate not in PARTICLES:
                continue

            if self._lookup(candidate, limit=1):
                return candidate

        return None

    def _lookup(self, reading: str, limit: int) -> list[KanjiCandidate]:
        if reading not in self._lookup_cache:
            self._lookup_cache[reading] = self.dictionary_client.lookup_by_reading(reading)
        return self._lookup_cache[reading][:limit]

    def _particle_at(self, text: str, index: int) -> str | None:
        char = text[index]
        if char not in PARTICLES:
            return None

        if index == 0:
            return char if len(text) == 1 else None

        remaining = text[index:]
        if self._lookup(remaining, limit=1):
            return None

        return char


def _is_hiragana(char: str) -> bool:
    return "\u3040" <= char <= "\u309f"
