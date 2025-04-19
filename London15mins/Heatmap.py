import folium
from folium.plugins import HeatMap
import pandas as pd

# 读取房价和POI数据
house_price_data_path = 'london_only_house_price.csv'  # 替换为你的文件路径
poi_data_path = 'london_all_pois.csv'  # 替换为你的文件路径

house_price_data = pd.read_csv(house_price_data_path)
poi_data = pd.read_csv(poi_data_path)

# 处理缺失值，确保数据不为空
house_price_data = house_price_data.dropna(subset=['lat', 'lon', 'price'])
poi_data = poi_data.dropna(subset=['lat', 'lon'])

# 确保经纬度数据是浮动类型
house_price_data['lat'] = house_price_data['lat'].astype(float)
house_price_data['lon'] = house_price_data['lon'].astype(float)
poi_data['lat'] = poi_data['lat'].astype(float)
poi_data['lon'] = poi_data['lon'].astype(float)

# 创建基础地图，设置在伦敦中心
map_center = [51.5074, -0.1278]

# 创建POI热力图
m_poi = folium.Map(location=map_center, zoom_start=12)

# 创建POI热力图数据（只包含经纬度）
poi_heat_data = [[row['lat'], row['lon']] for _, row in poi_data.iterrows()]

# 添加POI热力图到地图，使用内置的蓝色渐变
HeatMap(poi_heat_data, radius=25, blur=15, min_opacity=0.1).add_to(m_poi)

# 保存POI热力图
output_html_poi_only = 'london_poi_heatmap_blue_gradient.html'
m_poi.save(output_html_poi_only)

# 创建房价热力图
m_price_only = folium.Map(location=map_center, zoom_start=12)

# 创建房价热力图数据（包含经纬度和房价作为热力值）
house_price_heat_data = [[row['lat'], row['lon'], row['price']] for _, row in house_price_data.iterrows()]

# 添加房价热力图到地图，使用内置的红色渐变
HeatMap(house_price_heat_data, radius=35, blur=20, min_opacity=0.1).add_to(m_price_only)

# 保存房价热力图
output_html_price_only = 'london_price_heatmap_red_gradient.html'
m_price_only.save(output_html_price_only)

# 返回生成的两个 HTML 文件路径
output_html_poi_only, output_html_price_only
