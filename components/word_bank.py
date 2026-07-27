import re


class WordBank:
    def __init__(self, page):
        '''Initialize the WordBank component with the provided page.'''
        self.page = page
        self.hsk_tab = page.get_by_role("button", name="HSK Level")
        self.list_tab = page.get_by_role("button", name="My Lists")
        self.search_tab = page.get_by_role("button", name="Search", exact=True)
        self.search_input = page.get_by_role("searchbox", name="Search Chinese, pinyin, or")
        self.flashcards_practice_button = page.get_by_role("button", name="Flashcards Flip cards — test")
        self.multiple_choice_practice_button = page.get_by_role("button", name="Multiple Choice Pick the")
        self.listening_practice_button = page.get_by_role("button", name="Listening Hear the word and")
        self.match_practice_button = page.get_by_role("button", name="Match Pair characters with")
        self.tones_practice_button = page.get_by_role("button", name="Tones See the character —")
        self.handwriting_practice_button = page.get_by_role("button", name="Handwriting Preview strokes,")
        self.start_button = self.page.get_by_role("button", name=re.compile("Start Session"))
        
    def select_hsk_words(self, hsk=3, level=1, hsk_words=5, randomize=False):
        '''Select the specified HSK level.'''
        self.hsk_tab.click()
        self.page.get_by_role("button", name=f"HSK {hsk}.0").click()

        if level < 1:
            raise ValueError("Level must be 1 or higher.") 
        elif hsk == 3 and level > 9:
            raise ValueError("HSK 3.0 only has levels 1-9.")
        elif hsk == 2 and level > 6:
            raise ValueError("HSK 2.0 only has levels 1-6.")
        elif hsk == 3 and 7 <= level <= 9:
            self.page.get_by_role("button", name="–9").click()
        else:
            self.page.get_by_role("button", name=f"{level}", exact=True).click()
        
        self.page.get_by_role("button", name="Pick N").click()    
        number_words_input = self.page.get_by_role("spinbutton", name="Number of words")
        number_words_input.fill(str(hsk_words))
        
        if randomize:
            self.page.get_by_role("button", name="Random").click()
        else:
            self.page.get_by_role("button", name="Most common").click()
            
        self.page.get_by_role("button", name=re.compile(rf"Add.*{hsk_words}.*words?", re.IGNORECASE)).click()
        return self.page
    
    def select_my_lists(self):
        self.list_tab.click()
        self.page.get_by_role("button", name=re.compile("Saved Words")).click()
        return self.page
    
    def search_words(self, search_term = []):
        self.search_tab.click()
        for search in search_term:
            self.search_input.fill(search)
            self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(1).click()
            
    def start_session(self, practice_type="flashcards"):
        if practice_type == "flashcards":
            self.flashcards_practice_button.click()
        elif practice_type == "multiple_choice":
            self.multiple_choice_practice_button.click()
        elif practice_type == "listening":
            self.listening_practice_button.click()
        elif practice_type == "match":
            self.match_practice_button.click()
        elif practice_type == "tones":
            self.tones_practice_button.click()
        elif practice_type == "handwriting":
            self.handwriting_practice_button.click()
        else:
            raise ValueError(f"Invalid practice type: {practice_type}")
        
        self.start_button.click()
        
    def get_word_bank_words(self):
        '''Opens the word bank summary and returns the list of characters currently in it.'''
        self.page.get_by_role("button", name=re.compile(r"\d+ words? in bank")).click()
        word_buttons = self.page.locator("div.flex.flex-wrap.gap-1\\.5.max-h-40.overflow-y-auto button")
        count = word_buttons.count()
        return [word_buttons.nth(i).inner_text().strip() for i in range(count)]