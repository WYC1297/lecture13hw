import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import json

# ------------------ UI ------------------
st.set_page_config(
    page_title="台灣六大農業區天氣預報",
    page_icon="🌦",
    layout="wide"
)
st.title("🌦 台灣六大農業區 — 固定配色氣象儀表板")

# ------------------ 資料庫 ------------------
conn = sqlite3.connect("data.db")
df = pd.read_sql_query("SELECT * FROM weather ORDER BY location, date", conn)

df["date"] = pd.to_datetime(df["date"])
df["date_only"] = df["date"].dt.date

# ------------------ 讀 GeoJSON ------------------
geojson_path = "taiwan_agri_region_real.geojson"
with open(geojson_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# ------------------ 固定六區色彩 ------------------
region_colors = {
    "北部地區": "#4C9AFF",   # Blue
    "中部地區": "#FF7070",   # Red
    "南部地區": "#FFB347",   # Orange
    "東北部地區": "#8BC34A", # Green
    "東部地區": "#7E57C2",   # Purple
    "東南部地區": "#26A69A"  # Teal
}

df["color"] = df["location"].map(region_colors)

# ------------------ 日期 Slider ------------------
dates = sorted(df["date_only"].unique())

selected_date = st.slider(
    "📅 選擇日期",
    min_value=dates[0],
    max_value=dates[-1],
    value=dates[0]
)

filtered = df[df["date_only"] == selected_date]

# ------------------ Choropleth 地圖（最終穩定版 Mapbox） ------------------
st.subheader("🗺 六大農業區 — 高亮互動地圖（穩定版）")

fig = px.choropleth_mapbox(
    filtered,
    geojson=geojson_data,
    locations="location",
    featureidkey="properties.name",
    color="location",
    color_discrete_map=region_colors,
    mapbox_style="carto-positron",    # 不需要 token，正式可用
    zoom=5.6,
    center={"lat": 23.8, "lon": 121},
    opacity=0.7,
    hover_name="location",
    hover_data={
        "min_temp": True,
        "max_temp": True,
        "description": True,
    },
    height=650
)

# 🟦 美觀 tooltip（黑色卡片）
fig.update_layout(
    hoverlabel=dict(
        bgcolor="rgba(0,0,0,0.85)",
        font_size=16,
        font_color="white",
        bordercolor="white",
        align="left",
        namelength=-1
    )
)

# 🟦 格式化 tooltip
fig.update_traces(
    hovertemplate=
    "<b>%{hovertext}</b><br><br>" +
    "🌡️ 最低溫：%{customdata[0]}°C<br>" +
    "🌡️ 最高溫：%{customdata[1]}°C<br>" +
    "☁️ 天氣：%{customdata[2]}<extra></extra>"
)

# 🟦 Hover 高亮方式 = 區塊 hover 時自動變亮
# 利用 opacity + color → 讓 hover 更明顯
fig.update_traces(marker=dict(opacity=0.55))
fig.update_traces(hoverinfo="location+z")

# 🟦 外框（整個台灣輪廓）
fig.update_layout(
    mapbox_layers=[
        {
            "source": geojson_data,
            "type": "line",
            "color": "white",
            "line": {"width": 2}
        }
    ]
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

# ------------------ 折線圖 ------------------
st.subheader("📉 七天氣溫折線圖（依 max/min）")

selected_region = st.selectbox(
    "選擇地區",
    df["location"].unique()
)

df_region = df[df["location"] == selected_region]

line_fig = px.line(
    df_region,
    x="date_only",
    y=["min_temp", "max_temp"],
    markers=True,
    labels={"value": "氣溫 (°C)", "date_only": "日期"},
    color_discrete_sequence=["#4C9AFF", "#FF7070"],  # 統一樣式
    title=f"{selected_region} — 七天氣溫變化"
)

st.plotly_chart(line_fig, use_container_width=True)

# ------------------ 天氣卡片 ------------------
st.subheader(f"🌈 {selected_date} 各區詳細預報")

cols = st.columns(3)

weather_icon = {
    "晴": "☀️",
    "晴時多雲": "🌤",
    "多雲": "☁️",
    "多雲時晴": "🌥",
    "陰": "☁️",
    "陰短暫雨": "🌧",
    "多雲短暫雨": "🌧",
    "陰時多雲短暫雨": "🌦",
    "多雲時陰短暫雨": "🌦",
}

for i, (_, row) in enumerate(filtered.iterrows()):
    icon = weather_icon.get(row["description"], "🌦")

    with cols[i % 3]:
        st.markdown(
            f"""
            <div style="
                background:{region_colors[row['location']]};
                padding:20px;
                border-radius:12px;
                margin-bottom:15px;
                color:white;
                text-align:center;
                box-shadow:2px 2px 10px rgba(0,0,0,0.3);
            ">
                <h3>{row['location']}</h3>
                <div style="font-size:48px">{icon}</div>
                <h4>{row['description']}</h4>
                🌡️ <b>{row['min_temp']}°C ~ {row['max_temp']}°C</b>
            </div>
            """,
            unsafe_allow_html=True
        )
