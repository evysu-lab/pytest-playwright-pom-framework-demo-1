from playwright.sync_api._generated import Page
from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright
import pytest
import os
from datetime import datetime
import re
import base64



# 參數配置
def pytest_addoption(parser):
    # 環境參數
    parser.addoption(
        "--env", 
        action="store", 
        default="prod", 
        help="選擇環境: dev, staging, prod"
    )
    # 裝置參數 (新增)
    parser.addoption(
        "--platform", 
        action="store", 
        default="desktop", 
        help="選擇裝置: desktop, mobile"
    )


# 啟動時的初始環境
def pytest_configure(config):
    env = config.getoption("--env")
    device = config.getoption("--platform")
    print(f"\n" + "="*40)
    print(f"ENVIRONMENT : {env.upper()}")
    print(f"DEVICE : {device.upper()}")
    print(f"\n" +"="*40)


@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env")
    platform = request.config.getoption("--platform")
    
    env_config = {
        "dev": {"domain": "zh.wikipedia.org", "path": "zh-tw/"},
        "staging": {"domain": "en.wikipedia.org", "path": "wiki/"},#staging用英文wiki模擬切換狀態
        "prod": {"domain": "zh.wikipedia.org", "path": "zh-tw/"}
    }
    
    # 取得環境，預設給 prod
    current_conf = env_config.get(env, env_config["prod"])
    domain = current_conf["domain"]
    path = current_conf["path"]
    
    if platform == "mobile":
        domain = domain.replace("wikipedia", "m.wikipedia")
    
    final_url = f"https://{domain}/{path}"
    
    print(f"\n 環境: {env}, 裝置: {platform} -> {final_url}")
    return final_url



@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, request, playwright: Playwright):
    env = request.config.getoption("--env")
    platform = request.config.getoption("--platform")

    locale_map = {"staging": "en-US"}
    selected_locale = locale_map.get(env, "zh-TW")
    
    # 如果環境是 mobile，啟動Playwright的手機模擬功能
    if platform == "mobile":
            iphone = playwright.devices['iPhone 13']
            return {
                **browser_context_args,
                **iphone,
                "locale": selected_locale,
        }

    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": selected_locale,
    }

# 偵測失敗並貼標籤的Hook
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # 只有在執行測試call且report failed 時才動作
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            # 在 page object加上失敗記號
            page._test_failed = True
            test_name = re.sub(r'[^\w\-_]', '_', item.nodeid) 
            page._failed_test_name = test_name

# 檢查標籤並執行截圖的Fixture
@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page):
    yield 
    # yield後的程式碼會在測試結束後執行
    
    # 檢查這個 page 是否被上面的 Hook 貼了失敗標籤
    if hasattr(page, "_test_failed") and page._test_failed:
        # 建立截圖資料夾
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # 1. 取得測試名稱並縮短：只取最後一段，並限制在 30 個字元內
        full_name = getattr(page, "_failed_test_name", "unknown")
        short_name = full_name.split("_")[-1]  # 取得最後一個底線後的內容（通常是參數）
        if len(short_name) > 30:
            short_name = short_name[:30] # 避免參數過長導致報錯

        # 2. 格式化時間：MMDD，HHMMSS
        ts = datetime.now().strftime("%m%d_%H%M%S")
        
        # 3. 組合新檔名：FAIL_日期_測試名稱.png
        file_name = f"FAIL_{ts}_{short_name}.png"
        file_path = os.path.join(screenshot_dir, file_name)
        
        # 執行截圖
        page.screenshot(path=file_path)
        print(f"\n[自動截圖] 存檔成功: {file_name}")

# 把失敗截圖加到報告
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # 1. 準備路徑與檔名
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            ts = datetime.now().strftime("%m%d_%H%M%S")
            # 簡化檔名邏輯
            short_name = item.nodeid.split("::")[-1].split("[")[0] 
            file_name = f"FAIL_{ts}_{short_name}.png"
            file_path = os.path.join(screenshot_dir, file_name)

            # 2. 執行實體截圖存檔
            page.screenshot(path=file_path)
            
            # 3. 讀取剛才存好的檔案，轉成 base64 塞進 HTML 報告
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extras.append(pytest_html.extras.image(encoded_string))
                report.extras = extras

            print(f"\n[自動截圖] 已存檔並嵌入報告: {file_path}")

import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def api_request_context(playwright): 
    request_context = playwright.request.new_context(
        base_url="https://zh.wikipedia.org"
    )
    yield request_context
    request_context.dispose()