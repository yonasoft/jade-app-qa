import pytest


@pytest.fixture
def base_page(page):
    from pages.base_page import BasePage
    return BasePage(page)

@pytest.fixture
def start_home_page(page):
    page.goto("/", timeout=60000)
    return page