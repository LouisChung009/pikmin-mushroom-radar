# Pikmin Mushroom Radar

接手本專案請先讀 [STATUS.md](STATUS.md) 與 [LESSONS.md](LESSONS.md)。程式、測試、工作流程及資料皆保存於此儲存庫；自動取得真實遊戲觀測仍未完成，目前實際菇點為 0。

公開地圖：https://louischung009.github.io/pikmin-mushroom-radar/

本專案只發布可追溯的資料。社群回報不代表 Niantic 官方遊戲資料，也不是官方即時 API。

## 自有回報流程

1. 使用 GitHub Issue 表單「回報近期蘑菇觀測」提交本人親眼看到的菇點、UTC 時間、座標與種類/大小。
2. 提交者必須勾選親眼觀測及公開精確座標同意。不要提交私人場所、他人個資或推測資料。
3. Actions 會自動建立 `radar-approved` 核准標籤；維護者核對回報後才加上此標籤。沒有標籤的回報不會匯入。
4. GitHub Actions 每小時執行兩次，僅接受最近 90 分鐘、座標有效且同意欄位完整的核准回報，並寫入 `data/mushrooms.json`。
5. 地圖會標示「社群審核回報」。不會把 Gemini 搜尋結果當成遊戲實況，也不會讀取上游私有介面或帳號資料。

Issue 公開時，提交內容本身也可能公開。精確座標只有在勾選同意後才會進入地圖。可透過撤銷核准標籤，讓後續更新不再包含該筆回報。

## 目前限制

- 儲存庫目前為 public，Pages 已啟用。玩家可經 GitHub Issue 表單回報；此入口不代表自動掃描已完成。
- 本管線不是遊戲自動掃描器；若沒有人工提交並經維護者核准，近期菇點與巨大蘑菇數量應為 0。
- 固定點與其他即時 JSON feed 僅能接入已獲明確使用/再發布授權的來源。環境變數：`FIXED_SOURCE_URL`、`MUSHROOM_SOURCE_URL`。
- Pages 與收集工作已成功執行，但固定點與即時 feed 尚未設定；完整資料及瀏覽器互動驗收仍待完成。

## 本機驗收

```sh
python -m unittest discover -s tests -v
python audit_acceptance.py
```

獨立資料驗收在沒有真實新鮮回報時應回報 FAIL；不得用測試樣本或搜尋線索冒充實際菇點。

## 舊來源研究紀錄

- `odyliao-lab/pikmin-mush` 是社群掃描器專案，未取得其擁有者授權；本專案不依賴它的介面或資料。
- 逆向程式、hook 或私有遊戲介面不等於取得資料使用/再發布權。自有裝置擷取方式仍待確認相容性、授權與實機驗證；未部署或驗證任何 hook。
- 搜尋到的公開社群地圖也不會自動取得再發布授權，因此不會匯入未授權資料。
