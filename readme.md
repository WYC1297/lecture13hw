<div align="center">

# 🌦️ Taiwan Agricultural Region Weather Dashboard
## 六大農業區天氣預報 — CWA API + SQLite + Streamlit

<img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
<img src="https://img.shields.io/badge/Streamlit-App-red?logo=streamlit" />
<img src="https://img.shields.io/badge/SQLite-Database-green?logo=sqlite" />
<img src="https://img.shields.io/badge/GeoPandas-Map-green?logo=python" />
<img src="https://img.shields.io/badge/Plotly-Interactive%20Map-purple?logo=plotly" />

</div>

---

# 📚 目錄

- [📘 專案介紹](#-專案介紹)
- [📁 專案結構](#-專案結構)
- [🚀 安裝與執行](#-安裝與執行)
- [🌐 API 來源](#-api-來源)
- [🧊 SQLite 資料庫設計](#-sqlite-資料庫設計)
- [🗺️ 六大農業區地圖](#️-六大農業區地圖)
- [📸 預覽畫面](#-預覽畫面)
- [📄 授權](#-授權)

---

# 📘 專案介紹

本專案是一個互動式的台灣農業氣象儀表板。它會從**中央氣象署 (CWA)** 的開放資料平台抓取最新的農業氣象預報，將資料存入 **SQLite** 資料庫，並透過 **Streamlit** 框架以視覺化的方式呈現。

主要功能包含：
- **互動式地圖**：使用 Plotly 與 GeoJSON 繪製台灣六大農業區的等值面地圖 (Choropleth Map)，並可高亮顯示。
- **天氣資訊卡片**：以美觀的卡片風格顯示各區當日的天氣狀況、溫度範圍與天氣圖示。
- **多日期切換**：提供滑桿讓使用者輕鬆切換不同日期的天氣預報。
- **氣溫趨勢圖**：為指定地區繪製未來七天的最高與最低氣溫折線圖。
- **資料持久化**：透過 SQLite 儲存天氣資料，避免每次執行都需重新爬取。

---

# 📁 專案結構

```
.
├── 🌦️ cwa_crawler.py          # 從 CWA API 爬取天氣資料並存入 data.db
├── 🗺️ merge_agri_regions.py   # 將縣市 GeoJSON 合併為六大農業區
├── 🖥️ streamlit_app.py        # Streamlit 主應用程式
├── 🗃️ data.db                 # 儲存天氣資料的 SQLite 資料庫
├── 🌍 counties.geojson        # 原始台灣縣市地理圖資
├── 🌍 taiwan_agri_region_real.geojson # 合併後的六大農業區地理圖資
└── 📖 readme.md               # 本說明文件
```

---

# 🚀 安裝與執行

請依照以下步驟設定並執行本專案。

### 1. 前置需求

- Python 3.8 或更高版本
- `pip` 套件管理工具

### 2. 安裝依賴套件

在專案根目錄下開啟終端機，並執行以下指令安裝所有必要的 Python 套件：

```bash
pip install streamlit pandas requests geopandas plotly
```

### 3. 準備資料

專案需要先有天氣資料庫與地理圖資才能順利執行。

**A. 產生農業區地理圖資**
```bash
python merge_agri_regions.py
```
> 此指令會讀取 `counties.geojson` 並產生 `taiwan_agri_region_real.geojson`。

**B. 抓取天氣資料**
```bash
python cwa_crawler.py
```
> 此指令會呼叫 CWA API，並將最新的天氣預報資料寫入 `data.db`。

### 4. 啟動 Streamlit 應用程式

完成上述步驟後，執行以下指令啟動網頁應用程式：

```bash
streamlit run streamlit_app.py
```

應用程式將會在您的預設瀏覽器中開啟。

---

# 🌐 API 來源

本專案使用的氣象資料來自**交通部中央氣象署**的開放資料平台。

- **API 名稱**：農業氣象觀測資料 - 未來1週農業氣象預報
- **API ID**：`F-A0010-001`
- **授權金鑰**：`cwa_crawler.py` 中已包含範例金鑰，但建議申請自己的金鑰以確保穩定性。

---

# 🧊 SQLite 資料庫設計

天氣資料儲存於 `data.db` 的 `weather` 資料表中，其結構如下：

| 欄位 (Field) | 型別 (Type) | 說明 |
| :--- | :--- | :--- |
| `id` | `INTEGER` | 主鍵 (Primary Key) |
| `location` | `TEXT` | 地區名稱 (例如：北部地區) |
| `date` | `TEXT` | 預報日期 (YYYY-MM-DD) |
| `min_temp` | `REAL` | 最低溫度 (°C) |
| `max_temp` | `REAL` | 最高溫度 (°C) |
| `description`| `TEXT` | 天氣描述 (例如：晴時多雲) |

---

# 🗺️ 六大農業區地圖

`merge_agri_regions.py` 腳本會將台灣縣市合併為以下六大農業區，並產生對應的 GeoJSON 檔案，用於地圖繪製。

| 農業區 | 包含縣市 |
| :--- | :--- |
| **北部地區** | 臺北市, 新北市, 基隆市, 桃園市, 新竹縣, 新竹市, 宜蘭縣 |
| **中部地區** | 臺中市, 苗栗縣, 彰化縣, 南投縣, 雲林縣 |
| **南部地區** | 高雄市, 臺南市, 嘉義市, 嘉義縣, 屏東縣 |
| **東北部地區**| 宜蘭縣 |
| **東部地區** | 花蓮縣 |
| **東南部地區**| 臺東縣 |

---

# 📸 預覽畫面

*(您可以在此處插入應用程式的螢幕截圖)*

---

# 📄 授權

本專案採用 MIT 授權。詳情請見 `LICENSE` 檔案。
</div>