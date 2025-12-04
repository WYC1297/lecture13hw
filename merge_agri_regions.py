import geopandas as gpd
import pandas as pd

# 讀取你上傳的縣市 GeoJSON
source = "counties.geojson"
gdf = gpd.read_file(source)

# 找縣市名稱欄位
name_col = None
for col in gdf.columns:
    if "name" in col.lower():
        name_col = col
        break

if name_col is None:
    raise ValueError("找不到縣市名稱欄位，請確認 GeoJSON 欄位名稱！")

# 六大農業區分類
region_map = {
    "北部地區": ["臺北市", "新北市", "基隆市", "桃園市", "新竹縣", "新竹市", "宜蘭縣"],
    "中部地區": ["臺中市", "苗栗縣", "彰化縣", "南投縣", "雲林縣"],
    "南部地區": ["高雄市", "臺南市", "嘉義市", "嘉義縣", "屏東縣"],
    "東北部地區": ["宜蘭縣"],
    "東部地區": ["花蓮縣"],
    "東南部地區": ["臺東縣"]
}

merged_regions = []

for region_name, counties in region_map.items():
    sub = gdf[gdf[name_col].isin(counties)]
    merged = sub.dissolve()             # 合併 polygon
    merged["name"] = region_name
    merged_regions.append(merged)

# 合併所有六大區的 polygon
final_gdf = gpd.GeoDataFrame(pd.concat(merged_regions, ignore_index=True))

# 輸出 GeoJSON
output_path = "taiwan_agri_region_real.geojson"
final_gdf.to_file(output_path, driver="GeoJSON")

print("🎉 已成功輸出：", output_path)
