import pytest

# 使用 Playwright 內建的 api_request_context fixture
def test_get_wiki_summary(api_request_context):
    response = api_request_context.get(
        "https://zh.wikipedia.org/api/rest_v1/page/summary/Python"
    )
    
    assert response.ok
    assert response.status == 200
    
    data = response.json()
    assert data["title"] == "Python"
    assert "程式語言" in data["extract"]