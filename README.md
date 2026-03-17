# AWS 成本計算機

這是一個使用純前端 HTML/CSS/JavaScript 的 AWS 架構費用估算教學範例頁面，模擬某銀行在 AWS ap-east-1 的多 AZ 架構成本。

## 專案內容

- `tub_index.html`：主頁面，包含三個頁籤：架構圖、費用估算、計算說明。
- `tub_style.css`：整體 UI 樣式與排版。
- `tub_app.js`：動態互動與費用計算邏輯（可調整 CloudFront、ALB、NAT、EC2、EBS、Aurora、S3 參數）。

## 功能說明

1. 直觀的費用估算面板
2. 即時表格與總計更新
3. 切換不同情境與費用明細


## 如何執行

1. 在資料夾內啟動靜態伺服器（例如 `python -m http.server 8000`）。
2. 瀏覽器開啟 `http://localhost:8000/tub_index.html`。


