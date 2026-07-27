import pytest
from playwright.sync_api import Page
import re

@pytest.fixture
def base_page(page):
    from pages.base_page import BasePage
    return BasePage(page)

@pytest.fixture
def start_home_page(page):
    page.goto("/", timeout=60000)
    return page

@pytest.fixture
def start_practice_page(page):
    page.goto("/practice", timeout=60000)
    return page

@pytest.fixture
def practice_page(start_home_page: Page):
    '''Navigates to Practice and returns the raw page, ready for WordBank interactions.'''
    start_home_page.get_by_role("link", name="Practice").click()
    return start_home_page

@pytest.fixture
def list_with_five_words(start_home_page: Page):
    '''Adds 5 known words to the default Saved Words list via the UI.'''
    from pages.home_page import HomePage
    start_home_page.goto("/")
    home_page = HomePage(start_home_page)
    words = ["你好", "谢谢", "水", "学习", "爱"]
    for word in words:
        print(f"Searching: {word}")
        home_page.search_bar.search(word)
        print(f"Searched, clicking save for: {word}")
        first_result = start_home_page.locator("div.flex.flex-col.gap-2.mb-8").first
        first_result.get_by_role("button", name=re.compile("Save to")).click()
        print(f"Save clicked, clicking Saved Words checkbox for: {word}")
        start_home_page.get_by_text("Saved Words").click()
        print(f"Done with: {word}")
    return words