```markdown
# Playwright SDET Automation Framework (Python)
這是一個基於 Python 與 Playwright 打造的自動化測試框架，專門為多樣化的 Web 環境（多環境、多平台、多語系）所設計。本專案以維基百科作為測試目標，實作了從環境架構配置到錯誤診斷的完整自動化流程。

## 核心亮點
- **Page Object Model (POM)**: 實作架構分離，測試腳本僅專注於驗證邏輯，UI 定位與操作細節封裝於 Page Object 層，提升代碼重複使用性與維護效率。
- **BasePage 封裝**: 針對常用交互進行二次封裝，內建顯式等待機制，降低非同步加載導致的隨機失敗。
- **多平台模擬**: 透過 CLI 參數動態切換 Desktop 與 Mobile 瀏覽器上下文，驗證響應式網頁的行為。
- **多語系（i18n）相容性**: 針對不同語系間的 UI 變動與 URL 結構差異進行處理，確保測試腳本具備跨語系驗證能力。
- **並行執行運算**: 整合 `pytest-xdist` 插件，支援多核心並行測試，顯著優化測試套件的執行效率。
- **故障診斷機制**: 內建 Hook 處理器，當測試失敗時會自動擷取當下頁面截圖，存儲於 `reports/screenshots/` 路徑下。

## 技術棧
- **程式語言**: Python 3.12+
- **測試框架**: Pytest
- **驅動工具**: Playwright
- **報告產出**: pytest-html
- **自動化指令**: Makefile

## 技術挑戰與解決方案 (Technical Challenges & Solutions)
- **挑戰**: 處理行動版 Web 元素隱藏、動態加載與定位歧義。
- **解決方案**: 透過 POM 架構封裝特定 Locator 策略，針對手機版特定的選單與搜尋圖示實作條件式操作。

- **挑戰**: 切換語系時遇到 Strict Mode Violation，導致定位器指向多個元素。
- **解決方案**: 利用 CSS 層級定位與 `.first` 選擇器縮小範圍，並採用 `id` 或 `lang` 屬性確保元素選取的唯一性。

- **挑戰**: 提昇並行測試時的穩定性。
- **解決方案**: 調整 `pytest-xdist` 執行參數，確保每個 Worker 擁有獨立的 Browser Context，避免資源競爭。

## 快速上手
### 1. 安裝環境與依賴
```bash
make install

## 執行測試
本專案透過 Makefile 封裝了常用的執行模式，開發者無需記憶複雜的 pytest 指令：

- **make install**: 初次建立環境，自動安裝 requirements.txt 中的套件與 Playwright 瀏覽器核心。
- **make staging-m**: 在 Staging 環境執行 Mobile 平台測試（預設開啟並行模式）。
- **make prod-d**: 在 Production 環境執行 Desktop 平台測試（預設開啟並行模式）。
- **make clean**: 清理專案中的測試快取（.pytest_cache）、過期報告與失敗截圖。
- **make help**: 顯示所有可用的自動化指令及其詳細說明。

## 專案結構
本框架遵循 Page Object Model (POM) 設計模式，結構清晰且易於擴展：

```text
.
├── pages/               # Page Objects：封裝 UI 定位器與交互動作
│   ├── base_page.py     # 底層封裝，處理顯式等待與共通邏輯
│   └── wiki_page.py     # 維基百科專屬頁面邏輯
├── tests/               # Tests：存放測試腳本
│   ├── test_search.py   # 搜尋功能驗證
│   └── test_language.py # 多語系切換驗證
├── reports/             # 存放自動產出的報告與截圖
│   └── screenshots/     # 測試失敗時的自動截圖存檔
├── conftest.py          # Pytest 全域配置、Fixtures 與 Hook(截圖邏輯)
├── pytest.ini           # Pytest 設定檔，定義預設參數與標記
├── Makefile             # 工作流程自動化指令集
└── requirements.txt     # 專案依賴套件清單
