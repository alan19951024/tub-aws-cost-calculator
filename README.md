# AWS 成本計算機

這是一個使用純前端 HTML/CSS/JavaScript 的 AWS 架構費用估算教學範例頁面，模擬某銀行在 AWS ap-northeast-1 (Tokyo) 的多 AZ 架構成本。

## 專案內容

- `index.html`：主頁面，包含三個頁籤：專案架構圖、架構費用估算、計算詳細說明。
- `tub_style.css`：整體 UI 樣式與排版，包含卡片、切換標籤、全螢幕架構圖 modal 等樣式。
- `tub_app.js`：互動邏輯與動態成本計算（可調整 CloudFront、ALB、NAT、EC2、EBS、Aurora、S3 參數）。

## 功能說明

1. 架構圖 點擊放大：支援全螢幕 modal 展示架構圖。
2. 即時費用計算：依據輸入參數即時計算各服務與三層成本。
3. 答案隱藏/顯示：學習題可開關解答。
4. 三種情境試算：輕量、正常、業務高峰三個情境快速切換。




