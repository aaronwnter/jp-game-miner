from dataclasses import dataclass


@dataclass(frozen=True)
class CardDraft:
    expression: str
    reading: str
    meaning: str
    sentence: str
    source: str = ""
    tags: str = ""

    def validate(self) -> list[str]:
        missing_fields = []

        if not self.expression.strip():
            missing_fields.append("Expression is required.")
        if not self.reading.strip():
            missing_fields.append("Reading is required.")
        if not self.meaning.strip():
            missing_fields.append("Meaning is required.")
        if not self.sentence.strip():
            missing_fields.append("Sentence is required.")

        return missing_fields

    def parsed_tags(self) -> list[str]:
        tags: list[str] = []
        seen: set[str] = set()

        for tag in self.tags.replace(",", " ").split():
            cleaned_tag = tag.strip()
            if not cleaned_tag or cleaned_tag in seen:
                continue

            tags.append(cleaned_tag)
            seen.add(cleaned_tag)

        return tags

    def to_anki_fields(self) -> dict[str, str]:
        return {
            "Expression": self.expression,
            "Reading": self.reading,
            "Meaning": self.meaning,
            "Sentence": self.sentence,
            "Source": self.source,
            "Tags": self.tags,
        }
