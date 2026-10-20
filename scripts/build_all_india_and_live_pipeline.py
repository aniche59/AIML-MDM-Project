import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

BASE_DIR = "c:/Users/temp/Desktop/College/MDM"
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# ==========================================
# 1. DEFINE ALL-INDIA MANGANESE MINES DATABASE
# ==========================================
ALL_INDIA_MINES = [
    {
        "id": "MOIL_DONGRI_BUZURG",
        "name": "Dongri Buzurg Mine",
        "state": "Maharashtra",
        "district": "Bhandara",
        "operator": "MOIL Limited",
        "mine_type": "Open Cast",
        "latitude": 21.5317,
        "longitude": 79.7044,
        "geological_formation": "Sausar Group (Bichua / Mansar Formation)",
        "mineralogy": "Pyrolusite, Psilomelane, Cryptomelane, Braunite",
        "ibm_reserves_tonnes": 14583826,
        "weekly_planned_tonnes": 1000.0,
        "baseline_downtime_hours": 8.0,
        "baseline_blast_delay_hours": 2.0,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.74,
            "ferrous_mineral_ratio_b11_b8": 1.42,
            "clay_alteration_ratio_b11_b12": 1.68,
            "mean_pit_ndvi": 0.08
        },
        "description": "MOIL's flagship open-cast mechanized manganese mine situated in the Bhandara belt. Produces battery-grade manganese dioxide (MnO2) and high-grade lump ore."
    },
    {
        "id": "MOIL_BALAGHAT",
        "name": "Balaghat (Bharweli) Mine",
        "state": "Madhya Pradesh",
        "district": "Balaghat",
        "operator": "MOIL Limited",
        "mine_type": "Deep Underground (Asia's Deepest Mn Mine)",
        "latitude": 21.8656,
        "longitude": 80.2215,
        "geological_formation": "Sausar Group (Mansar Formation)",
        "mineralogy": "High-grade Braunite, Bixbyite, Hollandite",
        "ibm_reserves_tonnes": 18250000,
        "weekly_planned_tonnes": 850.0,
        "baseline_downtime_hours": 6.5,
        "baseline_blast_delay_hours": 1.5,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.82,
            "ferrous_mineral_ratio_b11_b8": 1.35,
            "clay_alteration_ratio_b11_b12": 1.71,
            "mean_pit_ndvi": 0.12
        },
        "description": "The deepest underground manganese mine in Asia (>380m vertical depth), producing premium ferro-manganese grade ore with over 46% Mn content."
    },
    {
        "id": "MOIL_GUMGAON",
        "name": "Gumgaon Mine",
        "state": "Maharashtra",
        "district": "Nagpur",
        "operator": "MOIL Limited",
        "mine_type": "Underground",
        "latitude": 21.3167,
        "longitude": 79.0500,
        "geological_formation": "Sausar Group (Lohangi / Mansar Formation)",
        "mineralogy": "Braunite, Jacobsite, Hausmannite",
        "ibm_reserves_tonnes": 4800000,
        "weekly_planned_tonnes": 350.0,
        "baseline_downtime_hours": 7.0,
        "baseline_blast_delay_hours": 2.0,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.65,
            "ferrous_mineral_ratio_b11_b8": 1.30,
            "clay_alteration_ratio_b11_b12": 1.55,
            "mean_pit_ndvi": 0.14
        },
        "description": "Historic Sausar belt underground mine operating down to the 6th level, supplying lump ore for captive domestic smelters."
    },
    {
        "id": "MOIL_TIRODI",
        "name": "Tirodi Mine",
        "state": "Madhya Pradesh",
        "district": "Balaghat",
        "operator": "MOIL Limited",
        "mine_type": "Open Cast",
        "latitude": 21.6881,
        "longitude": 79.6978,
        "geological_formation": "Sausar Group (Mansar Formation)",
        "mineralogy": "Braunite, Spessartite, Rhodonite",
        "ibm_reserves_tonnes": 6200000,
        "weekly_planned_tonnes": 520.0,
        "baseline_downtime_hours": 9.0,
        "baseline_blast_delay_hours": 2.5,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.88,
            "ferrous_mineral_ratio_b11_b8": 1.48,
            "clay_alteration_ratio_b11_b12": 1.62,
            "mean_pit_ndvi": 0.05
        },
        "description": "Large-scale open cast benches located on prominent ridge outcrops, known for world-class mineralogical specimens."
    },
    {
        "id": "MOIL_UKWA",
        "name": "Ukwa Mine",
        "state": "Madhya Pradesh",
        "district": "Balaghat",
        "operator": "MOIL Limited",
        "mine_type": "Underground",
        "latitude": 21.9686,
        "longitude": 80.4683,
        "geological_formation": "Sausar Group (Ukwa Horizon)",
        "mineralogy": "Fine-grained Braunite, Pyrolusite",
        "ibm_reserves_tonnes": 5100000,
        "weekly_planned_tonnes": 420.0,
        "baseline_downtime_hours": 6.0,
        "baseline_blast_delay_hours": 1.8,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.70,
            "ferrous_mineral_ratio_b11_b8": 1.38,
            "clay_alteration_ratio_b11_b12": 1.59,
            "mean_pit_ndvi": 0.16
        },
        "description": "Continuous synformal underground ore body extending over 5 km in length with extensive trackless decline mining."
    },
    {
        "id": "MOIL_MANSAR",
        "name": "Mansar Mine",
        "state": "Maharashtra",
        "district": "Nagpur",
        "operator": "MOIL Limited",
        "mine_type": "Open Cast & Underground",
        "latitude": 21.3967,
        "longitude": 79.2800,
        "geological_formation": "Sausar Group (Mansar Formation)",
        "mineralogy": "Braunite, Manganite, Hollandite",
        "ibm_reserves_tonnes": 5750000,
        "weekly_planned_tonnes": 480.0,
        "baseline_downtime_hours": 7.5,
        "baseline_blast_delay_hours": 2.2,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.76,
            "ferrous_mineral_ratio_b11_b8": 1.41,
            "clay_alteration_ratio_b11_b12": 1.65,
            "mean_pit_ndvi": 0.09
        },
        "description": "Combined open pit and shaft workings on the Ramtek-Mansar geological anticline."
    },
    {
        "id": "MOIL_CHIKLA",
        "name": "Chikla Mine",
        "state": "Maharashtra",
        "district": "Bhandara",
        "operator": "MOIL Limited",
        "mine_type": "Underground",
        "latitude": 21.5544,
        "longitude": 79.7431,
        "geological_formation": "Sausar Group (Sitalpur / Chikla Horizon)",
        "mineralogy": "Braunite, Bixbyite, Piedmonite",
        "ibm_reserves_tonnes": 6900000,
        "weekly_planned_tonnes": 580.0,
        "baseline_downtime_hours": 8.5,
        "baseline_blast_delay_hours": 2.1,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.72,
            "ferrous_mineral_ratio_b11_b8": 1.36,
            "clay_alteration_ratio_b11_b12": 1.60,
            "mean_pit_ndvi": 0.11
        },
        "description": "Underground operation adjacent to Dongri Buzurg, producing silicomanganese feedstock with high Mn:Fe ratio."
    },
    {
        "id": "TATA_OMC_JODA_BARBIL",
        "name": "Joda West & Barbil Complex",
        "state": "Odisha",
        "district": "Kendujhar (Keonjhar)",
        "operator": "Tata Steel / OMC",
        "mine_type": "Open Cast Mechanized",
        "latitude": 22.0167,
        "longitude": 85.4333,
        "geological_formation": "Iron Ore Group (IOG) / Bonai-Keonjhar Belt",
        "mineralogy": "Pyrolusite, Cryptomelane, Wad, Psilomelane",
        "ibm_reserves_tonnes": 12400000,
        "weekly_planned_tonnes": 1100.0,
        "baseline_downtime_hours": 9.5,
        "baseline_blast_delay_hours": 2.8,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.95,
            "ferrous_mineral_ratio_b11_b8": 1.58,
            "clay_alteration_ratio_b11_b12": 1.75,
            "mean_pit_ndvi": 0.04
        },
        "description": "Eastern India's most prolific manganese production zone. Lateritoid and strata-bound lens deposits within banded iron formations."
    },
    {
        "id": "JINDAL_OMC_KASIA",
        "name": "Kasia & Koira Complex",
        "state": "Odisha",
        "district": "Sundargarh",
        "operator": "Jindal Steel & Power / OMC",
        "mine_type": "Open Cast",
        "latitude": 22.0625,
        "longitude": 85.3528,
        "geological_formation": "Bonai-Keonjhar Horse-shoe Synclinorium",
        "mineralogy": "Manganese Oxides, Lateritic Mn-caps",
        "ibm_reserves_tonnes": 8600000,
        "weekly_planned_tonnes": 750.0,
        "baseline_downtime_hours": 8.0,
        "baseline_blast_delay_hours": 2.4,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.89,
            "ferrous_mineral_ratio_b11_b8": 1.52,
            "clay_alteration_ratio_b11_b12": 1.70,
            "mean_pit_ndvi": 0.06
        },
        "description": "High-tonnage surface extraction complex feeding steel manufacturing hubs of Kalinganagar and Rourkela."
    },
    {
        "id": "SMIORE_SANDUR_KUMARASWAMY",
        "name": "Sandur & Kumaraswamy Mines",
        "state": "Karnataka",
        "district": "Ballari (Bellary)",
        "operator": "Sandur Manganese & Iron Ores (SMIORE)",
        "mine_type": "Open Cast Semi-Mechanized",
        "latitude": 15.0833,
        "longitude": 76.5500,
        "geological_formation": "Dharwar Supergroup (Sandur Schist Belt)",
        "mineralogy": "Pyrolusite, Psilomelane, Wad, Braunite",
        "ibm_reserves_tonnes": 16500000,
        "weekly_planned_tonnes": 950.0,
        "baseline_downtime_hours": 8.5,
        "baseline_blast_delay_hours": 2.0,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.92,
            "ferrous_mineral_ratio_b11_b8": 1.60,
            "clay_alteration_ratio_b11_b12": 1.64,
            "mean_pit_ndvi": 0.03
        },
        "description": "South India's premier manganese basin, situated in the Sandur Schist Belt with low phosphorus manganese ore suitable for specialized ferroalloys."
    },
    {
        "id": "FACOR_GARIVIDI",
        "name": "Garividi & Chipurupalle Belt",
        "state": "Andhra Pradesh",
        "district": "Vizianagaram",
        "operator": "FACOR / Private Lessees",
        "mine_type": "Open Cast & Quarry",
        "latitude": 18.2833,
        "longitude": 83.5333,
        "geological_formation": "Eastern Ghats Mobile Belt (Khondalite Group)",
        "mineralogy": "Kodurite Suite (Braunite, Spandite, Rhodonite)",
        "ibm_reserves_tonnes": 3200000,
        "weekly_planned_tonnes": 300.0,
        "baseline_downtime_hours": 7.0,
        "baseline_blast_delay_hours": 1.5,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.68,
            "ferrous_mineral_ratio_b11_b8": 1.34,
            "clay_alteration_ratio_b11_b12": 1.58,
            "mean_pit_ndvi": 0.13
        },
        "description": "The historic Kodurite type-locality where manganese silicate-carbonate rocks occur within granulite facies khondalites."
    },
    {
        "id": "GMDC_SHIVRAJPUR",
        "name": "Shivrajpur Historical Mine",
        "state": "Gujarat",
        "district": "Panchmahal",
        "operator": "GMDC (Re-exploration Zone)",
        "mine_type": "Open Cast & Pit Re-development",
        "latitude": 22.4217,
        "longitude": 73.6183,
        "geological_formation": "Aravalli Supergroup (Champaner Series)",
        "mineralogy": "Pyrolusite, Braunite in Quartzites and Phyllites",
        "ibm_reserves_tonnes": 2100000,
        "weekly_planned_tonnes": 200.0,
        "baseline_downtime_hours": 6.5,
        "baseline_blast_delay_hours": 1.2,
        "spectral_indices": {
            "manganese_oxide_ratio_b4_b2": 1.78,
            "ferrous_mineral_ratio_b11_b8": 1.45,
            "clay_alteration_ratio_b11_b12": 1.61,
            "mean_pit_ndvi": 0.07
        },
        "description": "Western India's prominent historic manganese district currently being reassessed for beneficiation and secondary extraction."
    }
]

# Save all-India mines JSON
with open(os.path.join(PROCESSED_DIR, "all_india_mines.json"), "w") as f:
    json.dump(ALL_INDIA_MINES, f, indent=2)
print("Saved all_india_mines.json (12 Major Indian Manganese Mines)")

# ==========================================
# 2. TRAIN & BENCHMARK DUAL ML MODELS: RF vs XGBOOST
# ==========================================
csv_path = os.path.join(PROCESSED_DIR, "simulated_operations_weekly.csv")
df_ops = pd.read_csv(csv_path)

# Drop missing initial rows due to lagging
df_clean = df_ops.dropna(subset=['actual_tonnes_lag_1', 'rolling_mean_4']).copy()

feature_cols = [
    'planned_tonnes',
    'rainfall_mm_previous_week',
    'downtime_hours',
    'equipment_available_pct',
    'blast_delay_hours',
    'actual_tonnes_lag_1',
    'rolling_mean_4'
]

X = df_clean[feature_cols].values
y = df_clean['actual_tonnes'].values

# Chronological split: 80% train, 20% holdout (no shuffling)
split_idx = int(len(df_clean) * 0.8)
X_train, X_holdout = X[:split_idx], X[split_idx:]
y_train, y_holdout = y[:split_idx], y[split_idx:]

train_dates = df_clean['week_start'].iloc[:split_idx].values
holdout_dates = df_clean['week_start'].iloc[split_idx:].values

# Baseline: Trailing 4-week moving average
baseline_preds = df_clean['rolling_mean_4'].iloc[split_idx:].values
baseline_mae = mean_absolute_error(y_holdout, baseline_preds)
baseline_rmse = float(np.sqrt(mean_squared_error(y_holdout, baseline_preds)))
baseline_r2 = r2_score(y_holdout, baseline_preds)

# Model 1: Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=120, max_depth=8, random_state=26009)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_holdout)
rf_mae = mean_absolute_error(y_holdout, rf_preds)
rf_rmse = float(np.sqrt(mean_squared_error(y_holdout, rf_preds)))
rf_r2 = r2_score(y_holdout, rf_preds)

# Model 2: XGBoost Regressor
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.06,
    max_depth=4,
    subsample=0.85,
    colsample_bytree=0.85,
    random_state=26009
)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_holdout)
xgb_mae = mean_absolute_error(y_holdout, xgb_preds)
xgb_rmse = float(np.sqrt(mean_squared_error(y_holdout, xgb_preds)))
xgb_r2 = r2_score(y_holdout, xgb_preds)

print(f"=== MODEL EVALUATION (Chronological Holdout: {len(y_holdout)} weeks) ===")
print(f"Baseline (Trailing 4W Avg): MAE = {baseline_mae:.2f} t, RMSE = {baseline_rmse:.2f} t, R2 = {baseline_r2:.3f}")
print(f"Random Forest Regressor:    MAE = {rf_mae:.2f} t, RMSE = {rf_rmse:.2f} t, R2 = {rf_r2:.3f}")
print(f"XGBoost Regressor:          MAE = {xgb_mae:.2f} t, RMSE = {xgb_rmse:.2f} t, R2 = {xgb_r2:.3f}")

# Refit on all data for serving
rf_serving = RandomForestRegressor(n_estimators=120, max_depth=8, random_state=26009)
rf_serving.fit(X, y)

xgb_serving = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.06,
    max_depth=4,
    subsample=0.85,
    colsample_bytree=0.85,
    random_state=26009
)
xgb_serving.fit(X, y)

rf_importances = dict(zip(feature_cols, [round(float(v), 4) for v in rf_serving.feature_importances_]))
xgb_importances = dict(zip(feature_cols, [round(float(v), 4) for v in xgb_serving.feature_importances_]))

# Create enhanced forecast_results.csv with both models
df_holdout = df_clean.iloc[split_idx:].copy()
df_holdout['simulated_actual_tonnes'] = y_holdout
df_holdout['four_week_average_forecast_tonnes'] = np.round(baseline_preds, 2)
df_holdout['random_forest_forecast_tonnes'] = np.round(rf_preds, 2)
df_holdout['xgboost_forecast_tonnes'] = np.round(xgb_preds, 2)

df_holdout['rf_gap_tonnes'] = np.round(np.maximum(0, df_holdout['planned_tonnes'] - rf_preds), 2)
df_holdout['rf_shortfall_pct'] = np.round((df_holdout['rf_gap_tonnes'] / df_holdout['planned_tonnes']) * 100, 2)

df_holdout['xgb_gap_tonnes'] = np.round(np.maximum(0, df_holdout['planned_tonnes'] - xgb_preds), 2)
df_holdout['xgb_shortfall_pct'] = np.round((df_holdout['xgb_gap_tonnes'] / df_holdout['planned_tonnes']) * 100, 2)

out_cols = [
    'week_start', 'demo_site_id', 'planned_tonnes', 'simulated_actual_tonnes',
    'four_week_average_forecast_tonnes', 'random_forest_forecast_tonnes', 'xgboost_forecast_tonnes',
    'rf_gap_tonnes', 'rf_shortfall_pct', 'xgb_gap_tonnes', 'xgb_shortfall_pct', 'data_status'
]
df_holdout[out_cols].to_csv(os.path.join(PROCESSED_DIR, "forecast_results.csv"), index=False)
print("Updated forecast_results.csv with dual RF & XGBoost metrics")

# Enhanced Metrics JSON
metrics_dict = {
    "target": "simulated actual_tonnes",
    "total_usable_rows": len(df_clean),
    "train_rows": len(y_train),
    "holdout_rows": len(y_holdout),
    "train_start": str(train_dates[0]),
    "train_end": str(train_dates[-1]),
    "holdout_start": str(holdout_dates[0]),
    "holdout_end": str(holdout_dates[-1]),
    "split": "chronological 80/20 holdout; strictly no future data leakage or shuffling",
    "evaluation_method": "one-week-ahead rolling holdout evaluation",
    "models": {
        "baseline_trailing_4w": {
            "mae_tonnes": round(baseline_mae, 2),
            "rmse_tonnes": round(baseline_rmse, 2),
            "r2_score": round(baseline_r2, 3),
            "description": "Trailing 4-week rolling mean production (Non-ML naive benchmark)"
        },
        "random_forest": {
            "mae_tonnes": round(rf_mae, 2),
            "rmse_tonnes": round(rf_rmse, 2),
            "r2_score": round(rf_r2, 3),
            "feature_importances": rf_importances
        },
        "xgboost": {
            "mae_tonnes": round(xgb_mae, 2),
            "rmse_tonnes": round(xgb_rmse, 2),
            "r2_score": round(xgb_r2, 3),
            "feature_importances": xgb_importances
        }
    },
    "features": feature_cols,
    "feature_metadata": {
        "planned_tonnes": "Target production goal assigned for the operating week",
        "rainfall_mm_previous_week": "Observed 7-day cumulative rainfall from NASA/IMD/Open-Meteo telemetry",
        "downtime_hours": "Unscheduled haul truck, shovel, and crusher mechanical outage hours",
        "equipment_available_pct": "Percentage of operational fleet active during scheduled shifts",
        "blast_delay_hours": "Weather, misfire, or pit evacuation delay in explosive operations",
        "actual_tonnes_lag_1": "Production achieved in the immediately preceding operating week",
        "rolling_mean_4": "Trailing production trajectory over past month"
    }
}

with open(os.path.join(PROCESSED_DIR, "forecast_metrics.json"), "w") as f:
    json.dump(metrics_dict, f, indent=2)
print("Updated forecast_metrics.json with dual-model benchmark")

# ==========================================
# 3. CONSOLIDATE MASTER DATASET FOR THE BROWSER
# ==========================================
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
master_data["simulated_ops"] = df_ops.to_dict(orient="records")

# Forecast Results
df_fc = pd.read_csv(os.path.join(PROCESSED_DIR, "forecast_results.csv"))
master_data["forecast_results"] = df_fc.to_dict(orient="records")

# Forecast Metrics
master_data["forecast_metrics"] = metrics_dict

# All-India Mines
master_data["all_india_mines"] = ALL_INDIA_MINES

# Save master data JS and JSON
with open(os.path.join(PROCESSED_DIR, "minepulse_master_data.json"), "w") as f:
    json.dump(master_data, f, indent=2)

with open(os.path.join(PROCESSED_DIR, "minepulse_master_data.js"), "w") as f:
    f.write("window.MINEPULSE_DATA = " + json.dumps(master_data) + ";")

print("Master consolidated data generated successfully with All-India Mines & Dual ML Models!")
