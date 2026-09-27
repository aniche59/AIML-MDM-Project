import os
import json
import requests
import pandas as pd

# Define study area: Dongri Buzurg Manganese Mine, Bhandara District, Maharashtra
LATITUDE = 21.5317
LONGITUDE = 79.7044
LOCATION_NAME = "Dongri Buzurg Manganese Mine, Bhandara District, Maharashtra"
START_DATE = "20210101"  # YYYYMMDD
END_DATE = "20241231"    # YYYYMMDD

OUTPUT_DIR = os.path.join("data", "processed")
RAW_DIR = os.path.join("data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_nasa_power_rainfall(lat, lon, start, end):
    """
    Fetch daily precipitation (PRECTOTCORR) from NASA POWER Daily API.
    NASA POWER grid resolution: 0.5 deg (~50km regional grid).
    """
    print(f"Fetching daily weather/rainfall data for {LOCATION_NAME} ({lat}, {lon}) from NASA POWER API...")
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "PRECTOTCORR",  # Corrected Total Precipitation (mm/day)
        "community": "AG",            # Agroclimatology
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON"
    }
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    # Save raw json for provenance
    raw_filepath = os.path.join(RAW_DIR, "nasa_power_raw_rainfall.json")
    with open(raw_filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Raw API response saved to {raw_filepath}")
    
    precip_dict = data['properties']['parameter']['PRECTOTCORR']
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(list(precip_dict.items()), columns=['date_str', 'rainfall_mm'])
    df['date'] = pd.to_datetime(df['date_str'], format='%Y%m%d', errors='coerce')
    # If error in parsing format, try standard parse
    if df['date'].isnull().any():
        df['date'] = pd.to_datetime(df['date_str'])
        
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    # Filter fill values (-999 or negative)
    df['rainfall_mm'] = df['rainfall_mm'].apply(lambda x: max(0.0, float(x)) if x != -999 else 0.0)
    
    df['mine_id'] = "MOIL_DONGRI_BUZURG"
    df['location'] = LOCATION_NAME
    df['latitude'] = lat
    df['longitude'] = lon
    df['data_source'] = "NASA POWER Daily API (Regional Gridded 0.5deg)"
    df['data_status'] = "public_reference"
    
    # Final daily dataframe columns
    df_daily = df[['date', 'mine_id', 'location', 'latitude', 'longitude', 'rainfall_mm', 'data_source', 'data_status']]
    df_daily = df_daily.sort_values('date').reset_index(drop=True)
    
    return df_daily

def process_weekly_rainfall(df_daily):
    """
    Aggregate daily rainfall into weekly totals (week_start = Monday).
    """
    df_daily['date_dt'] = pd.to_datetime(df_daily['date'])
    # Resample to weekly starting on Monday
    # We assign each date to its week's Monday
    df_daily['week_start'] = df_daily['date_dt'].apply(lambda d: d - pd.Timedelta(days=d.weekday()))
    df_daily['week_start'] = df_daily['week_start'].dt.strftime('%Y-%m-%d')
    
    weekly = df_daily.groupby(['week_start', 'mine_id', 'location', 'latitude', 'longitude', 'data_source', 'data_status']).agg(
        rainfall_mm=('rainfall_mm', 'sum'),
        days_counted=('rainfall_mm', 'count'),
        max_daily_rainfall_mm=('rainfall_mm', 'max')
    ).reset_index()
    
    # Round rainfall to 2 decimal places
    weekly['rainfall_mm'] = weekly['rainfall_mm'].round(2)
    weekly['max_daily_rainfall_mm'] = weekly['max_daily_rainfall_mm'].round(2)
    
    # Keep complete 7-day weeks
    weekly = weekly[weekly['days_counted'] == 7].drop(columns=['days_counted'])
    weekly = weekly.sort_values('week_start').reset_index(drop=True)
    return weekly

def main():
    try:
        df_daily = fetch_nasa_power_rainfall(LATITUDE, LONGITUDE, START_DATE, END_DATE)
        
        # Save rainfall_daily.csv
        daily_csv_path = os.path.join(OUTPUT_DIR, "rainfall_daily.csv")
        df_daily.to_csv(daily_csv_path, index=False)
        print(f"Saved cleaned daily rainfall to {daily_csv_path} ({len(df_daily)} rows)")
        
        # Aggregate and save rainfall_weekly.csv
        df_weekly = process_weekly_rainfall(df_daily)
        weekly_csv_path = os.path.join(OUTPUT_DIR, "rainfall_weekly.csv")
        df_weekly.to_csv(weekly_csv_path, index=False)
        print(f"Saved aggregated weekly rainfall to {weekly_csv_path} ({len(df_weekly)} weeks)")
        
        # Display sample
        print("\n--- Weekly Rainfall Sample (First 5 weeks) ---")
        print(df_weekly.head())
        print("\n--- Weekly Rainfall Summary Stats ---")
        print(df_weekly['rainfall_mm'].describe())
        
    except Exception as e:
        print(f"Error processing rainfall data: {e}")
        raise e

if __name__ == "__main__":
    main()
