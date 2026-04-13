from app.core.text_normalizer import (
    normalize_for_display,
    normalize_for_tokenization,
)


def test_normalize_for_display_flattens_lines() -> None:
    text = "ポケットモンスターの\nせかいへ\nようこそ!"
    result = normalize_for_display(text)

    assert result == "ポケットモンスターのせかいへようこそ!"


def test_normalize_for_display_removes_empty_lines_and_outer_spaces() -> None:
    text = "  わたしの\n\n なまえは\n オダマキ!  "
    result = normalize_for_display(text)

    assert result == "わたしのなまえはオダマキ!"


def test_normalize_for_display_keeps_japanese_punctuation() -> None:
    text = "「あたらしい\nおともだちが\nできる!」"
    result = normalize_for_display(text)

    assert result == "「あたらしいおともだちができる!」"


def test_normalize_for_tokenization_removes_linebreaks_spaces_and_punctuation() -> None:
    text = "「あたらしい おともだちが できる!」\nなんて とても たのしみに してたの"
    result = normalize_for_tokenization(text)

    assert result == "あたらしいおともだちができるなんてとてもたのしみにしてたの"

def test_normalize_for_tokenization_removes_ascii_and_japanese_punctuation() -> None:
    text = "やった! ポケモンを つかまえた！？"
    result = normalize_for_tokenization(text)

    assert result == "やったポケモンをつかまえた"


def test_normalize_for_tokenization_removes_quotes_brackets_and_whitespace() -> None:
    text = " 「 きみは 」\n（ まだ ）『じぶんの』 ポケモンを もっていない "
    result = normalize_for_tokenization(text)

    assert result == "きみはまだじぶんのポケモンをもっていない"

def test_normalize_for_tokenization_repeated_punctuation() -> None:
    text = "!!! ??? ！！！ ？？？"
    result = normalize_for_tokenization(text)

    assert result == ""

def test_normalize_for_tokenization_handles_empty_string() -> None:
    assert normalize_for_tokenization("") == ""
