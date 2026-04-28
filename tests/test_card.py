from app.core.card import CardDraft


def test_valid_card_passes_validation() -> None:
    card = CardDraft(
        expression="冒険",
        reading="ぼうけん",
        meaning="adventure",
        sentence="これから ぼうけんが はじまる！",
    )

    assert card.validate() == []


def test_missing_required_fields_return_clear_validation_errors() -> None:
    card = CardDraft(expression="", reading="", meaning="", sentence="")

    assert card.validate() == [
        "Expression is required.",
        "Reading is required.",
        "Meaning is required.",
        "Sentence is required.",
    ]


def test_optional_source_and_tags_can_be_empty() -> None:
    card = CardDraft(
        expression="冒険",
        reading="ぼうけん",
        meaning="adventure",
        sentence="これから ぼうけんが はじまる！",
        source="",
        tags="",
    )

    assert card.validate() == []
    assert card.parsed_tags() == []


def test_parsed_tags_handles_commas_spaces_duplicates_and_empty_values() -> None:
    card = CardDraft(
        expression="冒険",
        reading="ぼうけん",
        meaning="adventure",
        sentence="これから ぼうけんが はじまる！",
        tags="pokemon, game-mining  vocab,, pokemon",
    )

    assert card.parsed_tags() == ["pokemon", "game-mining", "vocab"]


def test_to_anki_fields_uses_expected_field_names() -> None:
    card = CardDraft(
        expression="冒険",
        reading="ぼうけん",
        meaning="adventure",
        sentence="これから ぼうけんが はじまる！",
        source="Pokemon",
        tags="pokemon vocab",
    )

    assert card.to_anki_fields() == {
        "Expression": "冒険",
        "Reading": "ぼうけん",
        "Meaning": "adventure",
        "Sentence": "これから ぼうけんが はじまる！",
        "Source": "Pokemon",
        "Tags": "pokemon vocab",
    }
