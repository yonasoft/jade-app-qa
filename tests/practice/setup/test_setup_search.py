from components.word_bank import WordBank

COMMON_SEARCH_WORDS = ["你好", "谢谢", "水", "学习", "爱"]

def test_search_words_are_unique(practice_page):
    bank = WordBank(practice_page)
    bank.search_words(COMMON_SEARCH_WORDS)

    words = bank.get_word_bank_words()
    assert len(words) == 5, f"Expected 5 words in bank, got {len(words)}: {words}"
    assert len(set(words)) == len(words), f"Found duplicate words: {words}"