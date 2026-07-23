import re
from pages.base_page import BasePage
from typing import NamedTuple

class SearchResult(NamedTuple):
    simp: str
    trad: str
    pinyin: str
    term: str

class PageSearchBar:
    """Reusable across any page that has this search input/button."""
    def __init__(self, page: BasePage):
        self.page = page
        self.search_input = page.get_by_role("searchbox", name="Search Chinese characters,")
        self.input_toggle = page.get_by_role("button", name="Toggle Chinese input", exact=True)
        self.search_button = page.get_by_role("button", name="Search", exact=True)
        self.smart_chip = page.get_by_role("button", name="Smart")
        self.zh_chip = page.get_by_role("button", name="中文")
        self.pinyin_chip = page.get_by_role("button", name="Pinyin")
        self.english_chip = page.get_by_role("button", name="English")
        self.input_ui = page.locator("div.flex.border-b.border-zinc-800.overflow-x-auto")
        self.keyboard_input = self.input_ui.get_by_role("button", name=re.compile("Keyboard"))
        self.draw_input = self.input_ui.get_by_role("button", name=re.compile("Draw"))
        self.ocr_input = self.input_ui.get_by_role("button", name=re.compile("OCR"))
        self.voice_input = self.input_ui.get_by_role("button", name=re.compile("Voice"))
        self.paste_input = self.input_ui.get_by_role("button", name=re.compile("Paste"))

    def search(self, term):
        '''Search for a term using the search bar. Raises ValueError if term is empty.'''
        try:
            if not term:
                raise ValueError("Search term cannot be empty.")
            self.search_input.fill(term)
            self.search_button.click()
        except Exception as e:
            print(f"Error during search: {e}")
            raise
    
    def toggle_input_chip(self, chip_type):
        '''Toggle the input chip based on the provided chip_type. Raises ValueError for invalid chip_type.'''
        if chip_type == "smart":
            self.smart_chip.click()
        elif chip_type == "zh":
            self.zh_chip.click()
        elif chip_type == "pinyin":
            self.pinyin_chip.click()
        elif chip_type == "english":
            self.english_chip.click()
        else:
            raise ValueError(f"Invalid chip_type: {chip_type}")
        
    def toggle_input(self, input_type):
        '''Toggle the input method based on the provided input_type. Raises ValueError for invalid input_type.'''
        self.input_toggle.click()
        if input_type == "keyboard":
            self.keyboard_input.click()
        elif input_type == "draw":
            self.draw_input.click()
        elif input_type == "ocr":
            self.ocr_input.click()
        elif input_type == "voice":
            self.voice_input.click()
        elif input_type == "paste":
            self.paste_input.click()
        else:
            raise ValueError(f"Invalid input_type: {input_type}")


    def _extract_results_from_page(self, results_page):
        """Private helper — extracts SearchResult tuples from the currently loaded results page."""
        flex_results = results_page.locator("div.flex.flex-col.gap-2.mb-8")
        count = flex_results.count()
        results = []
        for i in range(count):
            result = flex_results.nth(i)
            spans = result.locator("span")
            span_count = spans.count()

            simp = spans.nth(0).inner_text()
            second = spans.nth(1).inner_text()
            third = spans.nth(2).inner_text() if span_count > 2 else None

            trad = second if third else simp
            pinyin = third if third else second
            term = result.locator("p").nth(0).inner_text()
            results.append(SearchResult(simp=simp, trad=trad, pinyin=pinyin, term=term))
        return results

    def get_search_results(self):
        '''Get search results for the first page only.'''
        self.search_button.click()
        self.page.wait_for_load_state("load")
        return self._extract_results_from_page(self.page)

    def get_all_search_results(self):
        '''Get all search results across every page.'''
        self.search_button.click()
        self.page.wait_for_load_state("load")

        all_results = []
        while True:
            all_results.extend(self._extract_results_from_page(self.page))
            next_link = self.page.get_by_role("link", name="Next page")
            if next_link.count() == 0 or next_link.get_attribute("aria-disabled") == "true":
                break
            next_link.click()
            self.page.wait_for_load_state("load")

        return all_results