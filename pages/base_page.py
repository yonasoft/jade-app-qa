class BasePage:
    def __init__(self, page):
        self.page = page

    def goto(self, path=""):
        self.page.goto(f"/{path}")
