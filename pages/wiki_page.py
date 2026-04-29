from playwright.sync_api import Page
from .base_page import BasePage


class WikipediaPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.page = page
        self.base_url = base_url
        self.search_input = page.locator("#searchInput")
        self.mobile_search_icon = page.locator("#searchIcon")
        # self.title_heading = page.locator("h1")
        self.title_heading = page.locator("#firstHeading")

    #帶往指定url
    def navigate(self):
        self.page.goto(self.base_url)
        self.click_if_visible(self.page.get_by_text("臺灣正體|English"))

    #搜尋關鍵字
    def search(self, text: str):
        if ".m.wikipedia.org" in self.base_url:
            self.wait_and_click(self.mobile_search_icon)
            mobile_input = self.page.locator("input[name='search']")
            self.wait_and_fill(mobile_input, text)
            mobile_input.press("Enter")
        else:
            self.wait_and_fill(self.search_input, text)
            self.search_input.press("Enter")

    #切換語系
    def switch_language(self, lang_code:str):
        lang_btn = self.page.locator("#p-lang-btn-checkbox")
        self.wait_and_click(lang_btn)

        target_lang = self.page.locator(f"a[lang='{lang_code}']").first
        self.wait_and_click(target_lang)