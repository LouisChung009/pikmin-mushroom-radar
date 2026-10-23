---
status: blocked_by_verified_data_source
updated: 2026-10-23
last_tool: Codex
---
# 專案現況與驗收

**總體 FAIL：可靠度修復已部署，但尚無經確認授權、含精確座標的近期巨大蘑菇資料來源。**

- 修復程式：1cdc2de0630cd2b0f7dfc13a2b7885e2b84c71e4。
- 來源實測補充：af978f52d5eb8783535e975961c93fbbbae4ed1e。
- 正式網站：https://louischung009.github.io/pikmin-mushroom-radar/
- Pages 部署 PASS：https://github.com/LouisChung009/pikmin-mushroom-radar/actions/runs/39916743869
- 收集後真實資料驗收 FAIL：https://github.com/LouisChung009/pikmin-mushroom-radar/actions/runs/39916442196
- 獨立驗收 FAIL：https://github.com/LouisChung009/pikmin-mushroom-radar/actions/runs/39916442332
- 第二次收集日誌顯示 No JSON changes to publish，空資料不再只更新時間戳：https://github.com/LouisChung009/pikmin-mushroom-radar/actions/runs/39916744554
- 本機22項Python測試通過；GitHub兩個工作流程的測試步驟也成功。
- 本機專用測試資料驗證：近期巨大菇顯示、巨大篩選、90分鐘過期移除、空資料FAIL、固定點篩選。測試資料未上線。
- 正式網站端到端驗證：地圖圖磚、兩種篩選、重新載入、空資料FAIL提示正常，瀏覽器錯誤紀錄為空。尚無真實巨大菇，不能宣稱真實巨大菇端到端驗收通過。

## 正式資料與設定
fixed_count=0、live_count=0、live_giant_count=0，status=no_observations、last_observed_at=null。
資料內容於2026-10-23 15:14:14 +08變更（新增欄位，並非取得觀測）。
search_sources.json仍為not_configured，searched_at=null、queries=0、count=0。
GitHub設定頁確認Repository Secrets與Environment Secrets都無設定；Actions自動提供的GITHUB_TOKEN不代表外部來源已配置。

## 修復內容
- 依正規化後有效觀測判定REQUIRE_LIVE_DATA，過期原始資料不算成功。
- 固定點不能建立活躍巨大菇；保留逐筆來源，修正同名來源錯配。
- 原子發布；資料內容相同時保留時間戳；加入last_observed_at。
- 外部feed需提供可查證的公開授權/許可URL，由維護者先核對內容；URL存在不等於自動完成法律審查。
- Gemini discovery接回排程，僅產出搜尋線索，絕不轉成遊戲觀測。
- 收集後執行資料驗收；獨立驗收增加push及每30分鐘排程。GitHub排程不保證準時。
- 前端每30秒過濾過期觀測，每分鐘重新載入，清楚呈現空資料FAIL。

## 真實來源與手機阻礙
完整證據見[SOURCE_RESEARCH.md](SOURCE_RESEARCH.md)。
mush.odyliao.cc/api/mushrooms在15:15:06 +08回傳24,722總筆數、500筆當頁資料，但500筆座標均為null，gps_access.authorized=false；未確認再發布授權，沒有繞過限制。
指定odyliao-lab/pikmin-mush目前404；同名bittieshsu專案README使用Root、Zygisk注入和定位覆寫，本次不採用。
其他明信片、OSM飾品地圖與社團抓取資料，均不能建立目前活躍巨大菇的合法可用來源。

官方ADB已成功連上實體CPH2783、遊戲已安裝且可擷取畫面。可見帳號Lv.7，官方蘑菇功能Lv.8解鎖，故本次沒有手機蘑菇詳情可驗證。未安裝Root、注入、GPS覆寫或第三方掃描器，未公開手機精確位置。

## 下一個必要條件
取得允許再發布的來源授權與精確座標接口，或有明確同意、可追溯、經維護者審核的第一手回報；再驗證持續更新、有效觀測、實際巨大菇與正式地圖。零資料不算完成。

---
# 2026-10-16歷史交接（以下內容可能已過時，以以上最新驗收為準）

# 專案交接與現況

## 目標
完成可持續取得真實 Pikmin Bloom 菇點與近期巨大蘑菇觀測的地圖；不得杜撰、不得把 AI 搜尋當遊戲實況、不得無授權再發布第三方資料、不增加費用。

## 接手入口
- 儲存庫：https://github.com/LouisChung009/pikmin-mushroom-radar （main，公開）
- 地圖：https://louischung009.github.io/pikmin-mushroom-radar/
- 先讀本檔、LESSONS.md、README.md，再讀實際程式與 Actions。
- 程式、測試、工作流程、公開資料皆已在 GitHub。本次原本工作目錄的 work/、outputs/ 為空，沒有額外本機程式需要搬移。
- GitHub 雲端可接手程式；手機 USB 與遊戲實機驗證需在可連接該手機的電腦操作，遠端 Codex 不會自動取得 USB 存取權。

## 已有實作
- radar.py：讀取經授權的 HTTPS JSON feeds；正規化、去重、時間有效性與巨大判斷，輸出 data/mushrooms.json。
- report_ingest.py：讀取明確同意、親眼觀測且維護者加 radar-approved 的 GitHub Issues；有效期 90 分鐘。
- .github/ISSUE_TEMPLATE/mushroom-report.yml：回報表單。
- index.html：Leaflet 地圖與篩選；尚無真實觀測。
- gemini_discovery.py：保留研究線索工具；例行收集 workflow 未呼叫 Gemini。
- audit_acceptance.py：獨立資料驗收。
- tests/、.github/workflows/radar.yml、independent-acceptance.yml：現有測試與自動化。

## 最新查證
- data/mushrooms.json 更新：2026-10-16T04:23:38.115379+00:00。
- fixed_count=0、live_count=0、live_giant_count=0，status=no_observations。
- fixed/live feeds 都是 not_configured。只有社群 Issues 接口，未形成自動遊戲掃描來源。
- 收集工作 success：https://github.com/LouisChung009/pikmin-mushroom-radar/actions/runs/38850375095
- Pages 部署 success：https://github.com/LouisChung009/pikmin-mushroom-radar/actions/runs/38850388508
- 上述成功只證明工作流程與部署成功，不表示真實資料接入完成；瀏覽器互動端到端驗收也尚未完成。
- radar-approved 建立程式已有 GET/404/POST 與 issues:write；前次標籤頁可能有快取，實際存在狀態待直接查證，不能據舊快取斷言不存在。

## 使用者現有裝置
- iPhone：可執行遊戲，但未查證可用的自動擷取方案。
- Android：OPPO A6x 5G，型號 CPH2783，ColorOS 16。
- 使用者照片顯示軟體版本 CPH2783_16.0.5.1200(EX01B110P02)；Android 系統版本未另行確認。
- 沒有 root。尚未連線、尚未檢查開發者選項／USB 偵錯，也未安裝掃描模組。
- 使用者已離開原本工作電腦，要改用另一個 Codex 接續；不要假設原主機的 USB／路徑可用。
- 不要公開原始手機照片、IMEI、序號、帳號或憑證。

## 先前研究的方法與限制
- odyliao-lab/pikmin-mush 的先前搜尋快照描述 root Android + Magisk/Zygisk + 特定遊戲版本 native hook + 裝置 Agent 上傳。
- 這是待研究的參考方法，不是本專案已建立或已驗證的掃描器，也未取得其程式或資料再發布授權。
- 本次 GitHub API 與 raw main/README.md 查詢回傳 404；不能單憑搜尋快照確認目前原始碼、授權或維護狀態。
- OPPO CPH2783 是否可解鎖／root、目前遊戲版本能否支援該方法，全都未查證。不得直接指示刷機或承諾可行。
- GitHub Actions 與 Pages 不會自己取得遊戲資料；必須有可用且被授權的真實來源或自有裝置擷取鏈路。

## 下一步
1. 在新環境 clone 儲存庫並確認 GitHub 連線。可先研究與開發，不要重新詢問已授權的接續工作。
2. 查證 OPPO CPH2783 的實際系統、遊戲版本與可用擷取方式。只有需本人操作的手機解鎖、USB 授權、登入才請使用者協助。
3. 若使用 USB，請使用者將手機接到新工作電腦；先做唯讀裝置檢查。不要擅自解鎖 bootloader、root、清除手機或購買服務。
4. 建立自有來源到收集器、JSON、地圖的完整鏈路，保留來源與觀測時間，完成真實數量及過期資料驗收。
5. 執行現有單元測試、獨立資料驗收及瀏覽器互動驗收。無真實來源時明確回報未完成，不以測試樣本充數。

## 驗收指令
```sh
python -m unittest discover -s tests -v
python audit_acceptance.py
```
獨立資料驗收在沒有真實近期資料時應 FAIL，不得為了綠燈放寬要求。

## 阻礙
自動遊戲資料來源未接通；OPPO 無 root 且相容性未知；沒有可直接使用的已授權第三方來源。

## 回報
2026-10-16 [Codex] 同步雲端交接文件與實際卡點；目前真實觀測 0 筆，專案仍未完成。

## 紀錄
2026-10-16 [Codex] 使用者要求完整放至 GitHub，供其他 Codex 接續。
