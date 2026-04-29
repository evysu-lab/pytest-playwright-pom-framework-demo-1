# pages/base_page.py
from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click_if_visible(self, selector_or_locator, timeout=3000):
        """嘗試點擊，如果元素沒出現也不會噴錯(popup dialog)"""
        try:
            if isinstance(selector_or_locator, str):
                self.page.click(selector_or_locator, timeout=timeout)
            else:
                selector_or_locator.click(timeout=timeout)
            return True
        except Exception:
            return False

    def wait_and_fill(self, locator: Locator, text: str, timeout=5000):
        """顯式等待元素可操作後再輸入內容"""
        locator.wait_for(state="visible", timeout=timeout)
        locator.fill(text)

    def wait_and_click(self, locator: Locator, timeout=5000):
        """顯式等待並點擊"""
        locator.wait_for(state="visible", timeout=timeout)
        locator.click()