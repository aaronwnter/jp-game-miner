import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from app.core.tokenization import KanjiCandidate


class JishoDictionaryClient:
    API_BASE_URL = "https://jisho.org/api/v1/search/words"

    def __init__(self, timeout_seconds: float = 4.0) -> None:
        self.timeout_seconds = timeout_seconds
        self.last_error: str | None = None

    def lookup_by_reading(self, reading: str, limit: int = 5) -> list[KanjiCandidate]:
        self.last_error = None

        if not reading:
            return []

        try:
            payload = self._fetch(reading)
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            self.last_error = f"Dictionary lookup failed: {error}"
            return []

        candidates = self._parse_candidates(payload, reading)
        candidates.sort(key=lambda candidate: (-candidate.score, len(candidate.expression)))
        return candidates[:limit]

    def _fetch(self, reading: str) -> dict:
        url = f"{self.API_BASE_URL}?keyword={quote(reading)}"
        request = Request(url, headers={"User-Agent": "jp-game-miner/0.1"})

        with urlopen(request, timeout=self.timeout_seconds) as response:
            body = response.read().decode("utf-8")

        return json.loads(body)

    def _parse_candidates(self, payload: dict, reading: str) -> list[KanjiCandidate]:
        candidates: list[KanjiCandidate] = []
        seen: set[tuple[str, str]] = set()

        for result_index, result in enumerate(payload.get("data", [])):
            meanings = self._extract_meanings(result)
            is_common = bool(result.get("is_common"))

            for japanese in result.get("japanese", []):
                candidate_reading = japanese.get("reading") or japanese.get("word") or ""
                if candidate_reading != reading:
                    continue

                expression = japanese.get("word") or candidate_reading
                if not expression:
                    continue

                key = (expression, candidate_reading)
                if key in seen:
                    continue

                seen.add(key)
                score = self._score_candidate(
                    expression=expression,
                    is_common=is_common,
                    result_index=result_index,
                )
                source_url = f"https://jisho.org/search/{quote(expression)}"

                candidates.append(
                    KanjiCandidate(
                        expression=expression,
                        reading=candidate_reading,
                        meanings=meanings,
                        is_common=is_common,
                        source_url=source_url,
                        score=score,
                    )
                )

        return candidates

    def _extract_meanings(self, result: dict) -> tuple[str, ...]:
        meanings: list[str] = []
        for sense in result.get("senses", []):
            for definition in sense.get("english_definitions", []):
                if definition and definition not in meanings:
                    meanings.append(definition)

        return tuple(meanings[:3])

    def _score_candidate(self, expression: str, is_common: bool, result_index: int) -> int:
        score = 1000 - result_index
        if is_common:
            score += 1000
        if _contains_kanji(expression):
            score += 500
        return score


def _contains_kanji(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)
