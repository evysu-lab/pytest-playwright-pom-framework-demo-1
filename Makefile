# --- 變數定義 ---
# 取得timestamp (例 0427_1100)
NOW = $(shell date +%m%d_%H%M)

# --self-contained-html 讓HTML報告包含 CSS/圖片
PYTEST_OPTS = -vs -n auto --html=reports/$(REPORT_NAME).html --self-contained-html

# 宣告偽目標，防止與檔名衝突
.PHONY: dev dev-m staging staging-m prod prod-m clean smoke

# --- 常用指令 (快捷鍵) ---

# 1. dev + 桌機
dev:
	$(eval REPORT_NAME=DEV_DESKTOP_$(NOW))
	pytest --env dev --platform desktop $(PYTEST_OPTS)

# 2. dev + 手機
dev-m:
	$(eval REPORT_NAME=DEV_MOBILE_$(NOW))
	pytest --env dev --platform mobile $(PYTEST_OPTS)


# 3. Staging (用英文版wiki模擬切換)+ 桌機
staging:
	$(eval REPORT_NAME=STAGING_DESKTOP_$(NOW))
	pytest --env staging --platform desktop $(PYTEST_OPTS)

# 4. Staging + 手機
staging-m:
	$(eval REPORT_NAME=STAGING_MOBILE_$(NOW))
	pytest --env staging --platform mobile $(PYTEST_OPTS)


# 5. Prod + 桌機
prod:
	$(eval REPORT_NAME=PROD_DESKTOP_$(NOW))
	pytest --env prod --platform desktop $(PYTEST_OPTS)


# 6. Prod + 手機
prod-m:
	$(eval REPORT_NAME=PROD_MOBILE_$(NOW))
	pytest --env prod --platform mobile $(PYTEST_OPTS)


# 冒煙測試
smoke:
	@echo "開始執行冒煙測試: prod, prod-mobile"
	-make prod
	-make prod-m

# ==========================================
# 工具指令 (Utility Commands)
# ==========================================

.PHONY: help install clean

help: ## 顯示所有指令說明
	@echo "可用指令列表:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## 初次安裝環境 (依賴項與瀏覽器)
	pip install -r requirements.txt
	playwright install chromium

clean: ## 清理測試產出的垃圾檔案與快取
	@echo "正在清理環境..."
	rm -rf reports/screenshots/*.png
	rm -rf reports/*.html
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "清理完成！"