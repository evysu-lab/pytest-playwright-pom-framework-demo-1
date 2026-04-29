def test_get_wiki_summary_netflix(api_request_context):
    # 拿到 Netflix 的 response
    response = api_request_context.get(
        "https://zh.wikipedia.org/api/rest_v1/page/summary/Netflix"
    )
    
    # 驗證連線成功
    assert response.ok
    assert response.status == 200
    
    data = response.json()
    
    # 驗證標題正確
    assert data["title"] == "Netflix"
    
    # 驗證摘要中包含 "OTT" (跨語系通用術語)
    assert "OTT" in data["extract"]