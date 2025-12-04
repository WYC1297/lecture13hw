import requests
import sqlite3

API_KEY = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
URL = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={API_KEY}&downloadType=WEB&format=JSON"

response = requests.get(URL)
data = response.json()

# 走正確 JSON 路徑
locations = data["cwaopendata"]["resources"]["resource"]["data"]["agrWeatherForecasts"]["weatherForecasts"]["location"]

# 建立 SQLite
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    date TEXT,
    min_temp REAL,
    max_temp REAL,
    description TEXT
)
""")

cursor.execute("DELETE FROM weather")

entries = []

for loc in locations:
    name = loc["locationName"]
    wx_daily = loc["weatherElements"]["Wx"]["daily"]
    max_daily = loc["weatherElements"]["MaxT"]["daily"]
    min_daily = loc["weatherElements"]["MinT"]["daily"]

    # 取第 1 天（今日）的預報
    for i in range(len(wx_daily)):
        date = wx_daily[i]["dataDate"]
        description = wx_daily[i]["weather"]
        max_temp = float(max_daily[i]["temperature"])
        min_temp = float(min_daily[i]["temperature"])

        entries.append((name, date, min_temp, max_temp, description))

cursor.executemany("""
INSERT INTO weather (location, date, min_temp, max_temp, description)
VALUES (?, ?, ?, ?, ?)
""", entries)

conn.commit()
conn.close()

print("✔ 資料已成功寫入 data.db！")
