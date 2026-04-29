import re
from playwright.sync_api import expect
from pages.wiki_page import WikipediaPage

# 切成英文網站，確認網址與標題正確變更
def test_switch_language_to_english(page, base_url):
    wiki = WikipediaPage(page, base_url)
    wiki.navigate()
    wiki.switch_language("en")
    
    # 驗證 1：網址是否變更為英文版
    # 使用re.compile 相容手機版 (.m.) 與桌面版
    expect(page).to_have_url(re.compile(r"https://en(\.m)?\.wikipedia\.org"))
    
    # 驗證 2：標題是否變更
    expect(wiki.title_heading).to_contain_text(re.compile(r"Main Page|Welcome", re.I))
    # page.pause()