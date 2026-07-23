# pages/home_page.py
from pages.base_page import BasePage
from components.page_search_bar import PageSearchBar

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.search_bar = PageSearchBar(page)