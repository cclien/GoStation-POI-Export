# GoStation-POI-Export
GoStation 站點匯出工具

### 匯出導航王自建點資料庫

Step1. 準備一份能動的 favorites.db

Step2. 執行 script 匯出站點資訊到 DB

`$ python gostation_navking.py favorites.db`

Note: script 可用來更新之前匯出過的資料庫 (利用 category_name 欄位判斷)