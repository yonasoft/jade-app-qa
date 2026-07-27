from components.word_bank import WordBank

def test_lists_words_are_unique(list_with_five_words, practice_page):
    bank = WordBank(practice_page)
    bank.select_my_lists()

    words = bank.get_word_bank_words()
    assert len(words) == 5, f"Expected 5 words in bank, got {len(words)}: {words}"
    assert len(set(words)) == len(words), f"Found duplicate words: {words}"
    assert set(words) == set(list_with_five_words), (
        f"Word bank contents don't match the list.\n"
        f"Bank: {sorted(words)}\nList: {sorted(list_with_five_words)}"
    )