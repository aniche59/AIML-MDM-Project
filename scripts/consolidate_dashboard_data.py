import os
import shutil
import json
import pandas as pd

BASE_DIR = "c:/Users/temp/Desktop/College/MDM"
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 1. Copy Person 1 files
p1_dir = os.path.join(BASE_DIR, "person 1")
gsi_geojson_src = os.path.join(p1_dir, "Manganese_Ore_deposits_in_India_and_its_salient_features.geojson")
ibm_csv_src = os.path.join(p1_dir, "ibm_mine_figures (1).csv")

if os.path.exists(gsi_geojson_src):
    shutil.copy(gsi_geojson_src, os.path.join(PROCESSED_DIR, "gsi_manganese.geojson"))
    print("Copied gsi_manganese.geojson")

if os.path.exists(ibm_csv_src):
    shutil.copy(ibm_csv_src, os.path.join(PROCESSED_DIR, "ibm_mine_figures.csv"))
    print("Copied ibm_mine_figures.csv")

# 2. Copy Person 3 files
p3_dir = os.path.join(BASE_DIR, "person_3_repo", "data", "processed")
for fname in ["simulated_operations_weekly.csv", "forecast_results.csv", "forecast_metrics.json", "forecast_example.json"]:
    src = os.path.join(p3_dir, fname)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(PROCESSED_DIR, fname))
        print(f"Copied Person 3 file: {fname}")

# 3. Create integrated master JSON for instantaneous, robust frontend loading without CORS issues
master_data = {}

# GSI GeoJSON
with open(os.path.join(PROCESSED_DIR, "gsi_manganese.geojson"), "r") as f:
    master_data["gsi_geojson"] = json.load(f)

# IBM CSV
df_ibm = pd.read_csv(os.path.join(PROCESSED_DIR, "ibm_mine_figures.csv"))
master_data["ibm_figures"] = df_ibm.to_dict(orient="records")

# Daily Rain
df_rain = pd.read_csv(os.path.join(PROCESSED_DIR, "rainfall_daily.csv"))
master_data["rainfall_daily"] = df_rain.to_dict(orient="records")

# Weekly Rain
df_rain_w = pd.read_csv(os.path.join(PROCESSED_DIR, "rainfall_weekly.csv"))
master_data["rainfall_weekly"] = df_rain_w.to_dict(orient="records")

# Sentinel Metadata
with open(os.path.join(PROCESSED_DIR, "sentinel2_context_metadata.json"), "r") as f:
    master_data["sentinel_metadata"] = json.load(f)

# Sentinel Coverage GeoJSON
with open(os.path.join(PROCESSED_DIR, "sentinel2_coverage.geojson"), "r") as f:
    master_data["sentinel_geojson"] = json.load(f)

# Simulated Operations
df_ops = pd.read_csv(os.path.join(PROCESSED_DIR, "simulated_operations_weekly.csv"))
master_data["simulated_ops"] = df_ops.to_dict(orient="records")

# Forecast Results
df_fc = pd.read_csv(os.path.join(PROCESSED_DIR, "forecast_results.csv"))
master_data["forecast_results"] = df_fc.to_dict(orient="records")

# Forecast Metrics
with open(os.path.join(PROCESSED_DIR, "forecast_metrics.json"), "r") as f:
    master_data["forecast_metrics"] = json.load(f)

# All-India Mines
all_mines_path = os.path.join(PROCESSED_DIR, "all_india_mines.json")
if os.path.exists(all_mines_path):
    with open(all_mines_path, "r") as f:
        master_data["all_india_mines"] = json.load(f)

# Save consolidated dataset as JS file and JSON file
with open(os.path.join(PROCESSED_DIR, "minepulse_master_data.json"), "w") as f:
    json.dump(master_data, f, indent=2)

with open(os.path.join(PROCESSED_DIR, "minepulse_master_data.js"), "w") as f:
    f.write("window.MINEPULSE_DATA = " + json.dumps(master_data) + ";")

print("Master consolidated data generated successfully!")
