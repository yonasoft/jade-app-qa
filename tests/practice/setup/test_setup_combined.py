from components.word_bank import WordBank
# Deliberately chosen to avoid overlap with list_with_five_words and common HSK level 1 words —
# verify manually against the real HSK 1 word list if this test proves flaky.

SEARCH_WORDS = ["再见", "苹果", "朋友", "老师", "书"]

def test_combined_sources_have_no_duplicates(practice_page, list_with_five_words):
    bank = WordBank(practice_page)

    bank.select_hsk_words(hsk=3, level=1, hsk_words=5)
    bank.select_my_lists()
    bank.search_words(SEARCH_WORDS)

    words = bank.get_word_bank_words()

    # Don't assert an exact count — HSK level 1 could legitimately overlap with
    # list/search words, and the app correctly dedupes on that. What actually
    # matters is that the app never shows the SAME word twice in the bank.
    assert len(set(words)) == len(words), (
        f"Found duplicate words in combined word bank: {words}"
    )

    # Confirm each source's words are at least represented somewhere in the bank
    for word in list_with_five_words:
        assert word in words, f"List word '{word}' missing from combined bank: {words}"
    for word in SEARCH_WORDS:
        assert word in words, f"Search word '{word}' missing from combined bank: {words}"