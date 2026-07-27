import pytest
from components.word_bank import WordBank


def test_hsk_words_are_unique(practice_page):
    bank = WordBank(practice_page)
    bank.select_hsk_words(hsk=3, level=1, hsk_words=5)

    words = bank.get_word_bank_words()
    assert len(words) == 5, f"Expected 5 words in bank, got {len(words)}: {words}"
    assert len(set(words)) == len(words), f"Found duplicate words: {words}"


def test_hsk_invalid_level_raises(practice_page):
    bank = WordBank(practice_page)
    with pytest.raises(ValueError):
        bank.select_hsk_words(hsk=3, level=0, hsk_words=5)


def test_hsk_level_out_of_range_raises(practice_page):
    bank = WordBank(practice_page)
    with pytest.raises(ValueError):
        bank.select_hsk_words(hsk=2, level=7, hsk_words=5)  # HSK 2.0 only goes to 6


def test_hsk_randomized_words_are_unique(practice_page):
    bank = WordBank(practice_page)
    bank.select_hsk_words(hsk=3, level=1, hsk_words=5, randomize=True)

    words = bank.get_word_bank_words()
    assert len(words) == 5, f"Expected 5 words in bank, got {len(words)}: {words}"
    assert len(set(words)) == len(words), f"Found duplicate words: {words}"