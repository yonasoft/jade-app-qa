from playwright.sync_api import Page, expect
import re
from conftest import start_home_page

def test_homepage_loads(start_home_page: Page):
    expect(start_home_page).to_have_title(re.compile("Jade Dictionary"))

def test_navigate_translate(start_home_page: Page):
    start_home_page.get_by_role("link", name="Translate").click()
    expect(start_home_page).to_have_title(re.compile("Translate"))
    expect(start_home_page).to_have_url(re.compile("/translate"))

def test_navigate_practice(start_home_page: Page):
    start_home_page.get_by_role("link", name="Practice").click()
    expect(start_home_page).to_have_title(re.compile("Practice"))
    expect(start_home_page).to_have_url(re.compile("/practice"))

def test_navigate_lists(start_home_page: Page):
    start_home_page.get_by_role("link", name="Lists").click()
    expect(start_home_page).to_have_title(re.compile("Word Lists"))
    expect(start_home_page).to_have_url(re.compile("/lists"))

def test_navigate_stats(start_home_page: Page):
    start_home_page.get_by_role("link", name="Stats").click()
    expect(start_home_page).to_have_title(re.compile("Stats"))
    expect(start_home_page).to_have_url(re.compile("/stats"))

def test_navigate_settings(start_home_page: Page):
    start_home_page.get_by_role("link", name="Settings").click()
    expect(start_home_page).to_have_title(re.compile("Settings"))
    expect(start_home_page).to_have_url(re.compile("/settings"))

def test_navigate_help(start_home_page: Page):
    start_home_page.get_by_role("link", name="Help").click()
    expect(start_home_page).to_have_title(re.compile("Help"))
    expect(start_home_page).to_have_url(re.compile("/help"))

# Navigates to landing page so root is different is in landing page,
def test_navigate_privacy(start_home_page: Page):
    start_home_page.get_by_role("link", name="Privacy").click()
    expect(start_home_page).to_have_title(re.compile("Privacy"))
    
# Navigates to landing page
def test_navigate_terms(start_home_page: Page):
    start_home_page.get_by_role("link", name="Terms").click()
    expect(start_home_page).to_have_title(re.compile("Terms"))

# Navigates to pLAY sTORE
def test_navigate_android(start_home_page: Page):
    with start_home_page.context.expect_page() as new_page_info:
        start_home_page.get_by_role("link", name="Android App").click()
    expect(new_page_info.value).to_have_url(url_or_reg_exp=re.compile(r"^https://play\.google\.com/store/apps/details\?id="))
    
# Navigates to landing page
def test_navigate_support(start_home_page: Page):
    with start_home_page.context.expect_page() as new_page_info:
        start_home_page.get_by_role("link", name="Support ♥").click()
    new_page = new_page_info.value
    expect(new_page).to_have_title(re.compile("Support"))

def test_navigate_wotd(start_home_page: Page):
    wotd_card = start_home_page.get_by_role("link", name=re.compile("Word of the Day"))
    wotd_character_before = wotd_card.locator("p").nth(1).inner_text()   # capture on homepage, before click

    wotd_card.click()

    expect(start_home_page).to_have_url(re.compile("/word/"))

    h1 = start_home_page.locator("h1")
    expect(h1).to_be_visible()
    expect(h1).to_contain_text(wotd_character_before)
    
def test_navigate_review(start_home_page: Page):
    start_home_page.get_by_role("link", name="Smart Review").click()
    expect(start_home_page).to_have_title(re.compile("Smart Review"))
    expect(start_home_page).to_have_url(re.compile("/review"))