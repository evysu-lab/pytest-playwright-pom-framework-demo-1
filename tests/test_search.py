import pytest
from pages.wiki_page import WikipediaPage
from playwright.sync_api import expect

@pytest.mark.parametrize("keyword",[
    "SpaceX",
    "故意失敗的關鍵字123"
])
def test_wiki_search(page, keyword,base_url):
    wiki = WikipediaPage(page,base_url)

    wiki.navigate()
    wiki.search(keyword)

    expect(wiki.title_heading).to_contain_text(keyword)

    page.wait_for_timeout(1000) #錄影時錄到最後一個動作