import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm

# 计算POI数量的函数
def count_nearby_pois(house_point, poi_df, radius_m=1250):
    # Convert radius from meters to degrees (1 degree ≈ 111320 meters)
    radius_deg = radius_m / 111320
    return poi_df.geometry.distance(house_point).lt(radius_deg).sum()

# 计算每个房产的POI数量
def compute_accessibility(house_data, poi_data):
    # Define POI types you're interested in
    poi_types = ['Park', 'School', 'Commer', 'Hospital', 'Transit']
    
    # Add new columns for each POI type (if not already present)
    for poi_type in poi_types:
        house_data[f'{poi_type.lower()}_access'] = 0

    # Loop through each house and calculate the number of nearby POIs
    for idx, row in tqdm(house_data.iterrows(), total=house_data.shape[0], desc="Calculating POI accessibility"):
        house_point = row['geometry']
        
        # Filter POIs by type and count them within the radius
        for poi_type in poi_types:
            poi_of_type = poi_data[poi_data['type'] == poi_type]
            count = count_nearby_pois(house_point, poi_of_type)
            house_data.at[idx, f'{poi_type.lower()}_access'] = count

    return house_data

# Load the house price data and POI data
def load_data():
    # Load house data (replace with your actual file path)
    house_data = pd.read_csv("london_only_house_price.csv")  # Update with actual path
    house_data['geometry'] = house_data.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    house_data = gpd.GeoDataFrame(house_data, geometry='geometry')

    # Load POI data (replace with your actual file path)
    poi_data = pd.read_csv("london_all_pois.csv")  # Update with actual path
    poi_data['geometry'] = poi_data.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    poi_data = gpd.GeoDataFrame(poi_data, geometry='geometry')

    return house_data, poi_data

# Main function to compute accessibility
def main():
    # Load house price data and POI data
    house_data, poi_data = load_data()

    # Step 1: Compute POI accessibility (count for 15-minutes walkability)
    house_data = compute_accessibility(house_data, poi_data)
    
    # Step 2: Append new columns to the original CSV
    house_data.to_csv("updated_london_house_price.csv", index=False)  # Save the new file with POI counts
    print("POI accessibility has been calculated and saved to 'updated_london_house_price.csv'.")

if __name__ == "__main__":
    main()