import re

from playwright.sync_api import Page, expect
import pytest
from pages.home_page import HomePage

# Each tuple: (search_term, chip_mode, description)
SEARCH_CASES = [
    ("你好", "zh", "Chinese characters -> Chinese chip"),
    ("你好", "smart", "Chinese characters -> Smart chip"),
    ("ni3 hao3", "pinyin", "Numbered pinyin -> Pinyin chip"),
    ("ni3 hao3", "smart", "Numbered pinyin -> Smart chip"),
    ("nǐ hǎo", "pinyin", "Toned pinyin -> Pinyin chip"),
    ("nǐ hǎo", "smart", "Toned pinyin -> Smart chip"),
    ("hello", "english", "English -> English chip"),
    ("hello", "smart", "English -> Smart chip"),
]


@pytest.fixture(params=SEARCH_CASES, ids=[case[2] for case in SEARCH_CASES])
def search_results_for_case(request, start_home_page: Page):
    search_term, chip_mode, _description = request.param
    home_page = HomePage(start_home_page)
    home_page.search_bar.toggle_input_chip(chip_mode)
    home_page.search_bar.search(search_term)
    results = home_page.search_bar.get_search_results()
    return search_term, chip_mode, results

def test_search_results_match_term(search_results_for_case):
    search_term, chip_mode, results = search_results_for_case

    # Numbered pinyin ("ni3 hao3") displays as accented pinyin ("nǐ hǎo") in the app.
    # Since we only test this one term, hardcode the expected accented form directly.
    NUMBERED_TO_ACCENTED = {
        "ni3 hao3": "nǐ hǎo",
    }
    comparison_term = NUMBERED_TO_ACCENTED.get(search_term, search_term)

    field_by_mode = {
        "zh": "trad",
        "pinyin": "pinyin",
        "english": "term",
    }

    if chip_mode == "smart":
        for result in results:
            assert (
                comparison_term in result.simp
                or comparison_term in result.trad
                or comparison_term in result.pinyin
                or comparison_term in result.term
            ), f"'{comparison_term}' (smart) not found in any field of result: {result}"
    else:
        expected_field = field_by_mode[chip_mode]
        for result in results:
            actual_value = getattr(result, expected_field)
            assert comparison_term in actual_value, (
                f"'{comparison_term}' ({chip_mode} mode) expected in '{expected_field}' "
                f"but got: {result}"
            )
            
def test_input_toggles(start_home_page: Page):
    home_page = HomePage(start_home_page)
    home_page.search_bar.input_toggle.click()

    expect(home_page.search_bar.keyboard_input).to_be_visible(timeout=10000)

    home_page.search_bar.draw_input.click()
    expect(home_page.search_bar.draw_input).to_have_class(re.compile("border-green-400"))

    home_page.search_bar.ocr_input.click()
    expect(home_page.search_bar.ocr_input).to_have_class(re.compile("border-green-400"))

    home_page.search_bar.voice_input.click()
    expect(home_page.search_bar.voice_input).to_have_class(re.compile("border-green-400"))

    home_page.search_bar.paste_input.click()
    expect(home_page.search_bar.paste_input).to_have_class(re.compile("border-green-400"))

    home_page.search_bar.keyboard_input.click()
    expect(home_page.search_bar.keyboard_input).to_have_class(re.compile("border-green-400"))