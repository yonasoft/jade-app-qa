# pages/home_page.py
import re

from components.word_bank import WordBank
from pages.base_page import BasePage


class PracticePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.word_bank = WordBank(page)

        