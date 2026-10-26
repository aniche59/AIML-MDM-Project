# MinePulse — AI/ML & Space Technology for Manganese Reserve Planning & Shortfall Mitigation

[![Smart India Hackathon](https://img.shields.io/badge/SIH%202024-Problem%20SIH26009-E07A5F?style=for-the-badge&logo=target)](https://www.sih.gov.in/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-D9825B?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Models-Random%20Forest%20%7C%20XGBoost-8CB399?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Remote Sensing](https://img.shields.io/badge/Satellite-ESA%20Sentinel--2%20MSI-7EB0D5?style=for-the-badge&logo=esa)](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2)
[![License: MIT](https://img.shields.io/badge/License-MIT-E5B27D?style=for-the-badge)](LICENSE)

> **MinePulse** is an end-to-end geospatial and predictive mining intelligence platform developed for **Smart India Hackathon (Problem ID: SIH26009)** under the theme *"Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls"*. 
>
> It combines **Sentinel-2 multispectral satellite remote sensing**, **real-time micro-meteorological sensor telemetry**, **physics-informed mining domain feature engineering**, and **dual-tree ensemble machine learning (Random Forest & XGBoost)** to map manganese deposit context across India and forecast weekly production shortfalls before they freeze operations.

---

## 📌 Executive Summary

Manganese is a vital strategic mineral: over **90% of global manganese output** is indispensable for steel manufacturing (as a deoxidizer and alloying agent), while high-purity electrolytic manganese dioxide (EMD) is an essential cathode precursor for **Lithium-ion NMC (Nickel-Manganese-Cobalt) electric vehicle batteries**.

India holds significant manganese resources, primarily operated by **MOIL Limited**, **OMC**, **Tata Steel**, and **SMIORE**. However, open-cast and underground mines face acute production challenges:
1. **Severe Monsoon Disruptions:** Unpredictable precipitation floods open pits, softens haul roads, and impairs heavy machinery cycle times.
2. **Explosive Blasting Bottlenecks:** Directorate General of Mines Safety (DGMS) statutory safety guidelines mandate blasting halts during lightning and extreme weather.
3. **Unscheduled Fleet Downtime:** Haul truck tire degradation on slick wet clay and excavator outages cause cascade delays.
4. **Geological Prospectivity Blindspots:** Surface vegetation and overburden mask prospective manganese ore horizons, complicating exploration targeting.

**MinePulse** addresses this dual challenge by providing:
- **Space-borne Surface Alteration Screening:** 10m–20m multispectral band ratios (Mn/Fe Oxides, Hydrothermal Clay Alteration, and Pit Footprint NDVI) from Copernicus Sentinel-2.
- **National Basin Geospatial Hub:** An interactive geospatial dashboard tracking **12 major manganese mines** across **5 geological belts**, alongside **32 documented GSI deposit occurrences** and **official IBM reported reserves**.
- **Physics-Informed Production Shortfall Forecaster:** A dual-model ML engine (Random Forest vs. XGBoost) achieving **25.02 tonnes MAE (30.8% lower error than baseline)** on chronologically held-out operational data.
- **Interactive "What-If?" Decision Simulator:** Real-time simulation of proactive interventions (dispatching auxiliary pumps, deploying maintenance crews, rescheduling blasts) to calculate net tonnage recovered.
- **DGMS Operational Shift Advisory:** Automated compliance report generator for mine managers and shift in-charges.

---

## 🗺️ Where It Works: All-India Geographical & Geological Coverage

MinePulse is not restricted to a single site; it covers the major manganese-bearing provinces of India, spanning **12 premier industrial mining hubs across 5 states**:

| Mine Name | Operator | District, State | Mining Method | Geological Formation / Belt | IBM Reserves / Resources | Weekly Target |
|---|---|---|---|---|---|---|
| **Dongri Buzurg Mine** | MOIL Ltd. | Bhandara, Maharashtra | Open Cast Mechanized | Sausar Group (Mansar/Bichua) | 14,583,826 t | 1,000 t |
| **Balaghat (Bharweli)** | MOIL Ltd. | Balaghat, Madhya Pradesh | Deep Underground (>380m) | Sausar Group (Mansar) | 18,250,000 t | 850 t |
| **Gumgaon Mine** | MOIL Ltd. | Nagpur, Maharashtra | Underground | Sausar Group (Lohangi) | 4,800,000 t | 350 t |
| **Tirodi Mine** | MOIL Ltd. | Balaghat, Madhya Pradesh | Open Cast | Sausar Group (Mansar) | 6,200,000 t | 520 t |
| **Ukwa Mine** | MOIL Ltd. | Balaghat, Madhya Pradesh | Underground | Sausar Group (Ukwa Horizon) | 5,100,000 t | 420 t |
| **Mansar Mine** | MOIL Ltd. | Nagpur, Maharashtra | Open Cast & Underground | Sausar Group (Anticlinal Crest) | 5,750,000 t | 480 t |
| **Chikla Mine** | MOIL Ltd. | Bhandara, Maharashtra | Underground | Sausar Group (Sitalpur) | 6,900,000 t | 580 t |
| **Joda West & Barbil** | Tata Steel / OMC | Keonjhar, Odisha | Open Cast Mechanized | Bonai-Keonjhar Iron Ore Group | 12,400,000 t | 1,100 t |
| **Kasia & Koira** | Jindal / OMC | Sundargarh, Odisha | Open Cast | Bonai-Keonjhar Synclinorium | 8,600,000 t | 750 t |
| **Sandur & Kumaraswamy**| SMIORE | Ballari, Karnataka | Open Cast Semi-Mechanized | Dharwar (Sandur Schist Belt) | 16,500,000 t | 950 t |
| **Garividi Belt** | FACOR / Private | Vizianagaram, Andhra Pradesh | Open Cast Quarry | Khondalite (Kodurite Suite) | 3,200,000 t | 300 t |
| **Shivrajpur Mine** | GMDC | Panchmahal, Gujarat | Open Cast Re-development | Champaner Series (Aravalli) | 2,100,000 t | 200 t |

Furthermore, the geospatial layer maps **32 national documented occurrence points** cataloged by the Geological Survey of India (GSI) with deposit density heatmaps.

---

## ⚙️ How It Works: System Architecture & Data Engineering

```
                          ┌────────────────────────────────────────────────────────┐
                          │                   MINEPULSE PIPELINE                   │
                          └────────────────────────────────────────────────────────┘
                                                       │
        ┌──────────────────────────────────────────────┼──────────────────────────────────────────────┐
        │                                              │                                              │
        ▼                                              ▼                                              ▼
┌──────────────────────────────┐       ┌──────────────────────────────┐       ┌──────────────────────────────┐
│  1. Space Tech & Satellite   │       │   2. Real-Time Telemetry     │       │   3. Ground Geological Data  │
│  • Copernicus Sentinel-2 MSI │       │   • Open-Meteo High-Res ERA5 │       │   • GSI 32 Occurrence Points │
│  • Spectral Band Ratios:     │       │   • Live Temp, Rain (mm/h)   │       │   • IBM Minerals Yearbook    │
│    - Mn/Fe Oxide (B4/B2)     │       │   • Soil Moisture (0-7cm)    │       │     2024 UNFC Reserves       │
│    - Hydrothermal (B11/B12)  │       │   • Wind Speed (km/h)        │       │   • Pit Bench Footprints     │
│    - Ferrous Ratio (B11/B8)  │       │   • Strictly Digital Sensing │       │                              │
│    - Pit Footprint NDVI      │       │                              │       │                              │
└──────────────┬───────────────┘       └──────────────┬───────────────┘       └──────────────┬───────────────┘
               │                                      │                                      │
               └──────────────────────────────────────┼──────────────────────────────────────┘
                                                      │
                                                      ▼
                                       ┌──────────────────────────────┐
                                       │ 4. Physics Feature Pipeline  │
                                       │ • 7-Day Rolling Resampling   │
                                       │ • Pit Sump Flooding (SFRI)   │
                                       │ • Haul Road Degradation      │
                                       │ • DGMS Blasting Safety Model │
                                       │ • Autoregressive Momentum    │
                                       └──────────────┬───────────────┘
                                                      │
                                                      ▼
                                       ┌──────────────────────────────┐
                                       │  5. Dual-Tree ML Inference   │
                                       │ • Random Forest Regressor    │
                                       │ • XGBoost Gradient Boosting  │
                                       │ • 80/20 Chronological Split  │
                                       │ • Holdout MAE: 25.02 t       │
                                       └──────────────┬───────────────┘
                                                      │
                                                      ▼
                                       ┌──────────────────────────────┐
                                       │ 6. Interactive Decision Hub  │
                                       │ • Real-Time Leaflet GIS Map  │
                                       │ • What-If Scenario Simulator │
                                       │ • Net Tonnage Recovery Calc  │
                                       │ • Shift Advisory Generator   │
                                       └──────────────────────────────┘
```

### 1. Space Technology & Multispectral Mineral Prospectivity
Optical satellite imagery cannot penetrate underground rocks directly, but it reliably detects diagnostic surface alteration halos, gossan caps, and excavation scars. Using **Copernicus Sentinel-2 Level-2A (10m–20m)** surface reflectance bands:
- **Manganese / Iron Oxide Alteration Index ($\text{Band 4} / \text{Band 2}$):** Delineates ferric oxide gossans and secondary Mn supergene enrichment caps where intense blue (B2) absorption contrasts with high red (B4) reflectance.
- **Hydrothermal Clay & Carbonate Alteration ($\text{Band 11} / \text{Band 12}$):** Isolates argillic/phyllitic alteration haloes surrounding stratiform manganese horizons.
- **Ferrous Mineral Ratio ($\text{Band 11} / \text{Band 8}$):** Flags silicate and carbonate facies associated with proto-ore beds.
- **Normalized Difference Vegetation Index ($\text{NDVI} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}}$):** Separates dense forest canopies from exposed open-pit benches and mine waste dumps.

### 2. Live Atmospheric Telemetry & The "API vs. Data Science" Distinction
A frequent academic question is: *"Is the external weather API doing your AI/ML?"*
**The answer is an emphatic NO.**
- **The External API (Open-Meteo):** Functions strictly as a **remote digital weather station**. It streams raw physical metrics at the mine's exact coordinates: ambient temperature (°C), precipitation (mm/h), wind speed (km/h), and volumetric topsoil moisture ($0-7\text{ cm}$ in $\text{m}^3/\text{m}^3$). It has zero knowledge of mines, manganese, or production shortfalls.
- **Our Data Science Codebase:** Performs all temporal aggregation, physical unit normalization, domain-specific feature engineering, and ensemble ML inference:
  - **Pit Sump Flooding & Water Ponding Index ($\text{SFRI}$):**
    $$\text{SFRI} = \min\left(100, \left(\frac{\text{Precipitation}_{7\text{d}}}{50} \times 0.6 + \frac{\text{Soil Moisture}_{0-7\text{cm}}}{0.45} \times 40\right)\right)$$
  - **Haul Road Slipperiness & Machine Degradation Multiplier:**
    $$\text{Degradation Factor} = 1.0 + \max\left(0, (\text{Soil Moisture} - 0.22) \times 2.2\right)$$
    Translates wet montmorillonite/clay soil physics into haul truck tire traction loss, cycle turnaround delay, and heavy transmission wear.
  - **DGMS Statutory Blasting Clearance Model:** Evaluates lightning risk and surface water ponding to trigger safety blasting suspensions.

### 3. Dual-Tree Machine Learning Benchmark
Models were trained on **208 operating weeks** (2021–2024) using a strict **chronological 80/20 train/holdout split** (163 training weeks, 41 holdout weeks; strictly no random shuffling or future leakage):

| Model / Architecture | Holdout MAE | Holdout RMSE | $R^2$ Score | Performance vs. Baseline |
|---|---|---|---|---|
| **Trailing 4-Week Moving Average (Baseline)** | 36.16 tonnes | 50.50 tonnes | 0.127 | Benchmark (Naive heuristic) |
| **Random Forest Regressor (120 Trees, max_depth=8)** | 26.12 tonnes | 31.68 tonnes | 0.656 | **27.8% Error Reduction** |
| **XGBoost Regressor (100 Trees, lr=0.06, depth=4)** | **25.02 tonnes** | **30.02 tonnes** | **0.691** | **30.8% Error Reduction (Champion)** |

#### Model Feature Importances (Tree Gini Importance):
1. **Prior Week Rainfall:** **$38.6\%$** (Open-cast sump inundation & haul road churn)
2. **Planned Target Tonnes:** **$22.0\%$** (Production quota scaling)
3. **Blasting Delay Hours:** **$16.3\%$** (Explosive fragmentation bottleneck)
4. **Machinery Downtime Hours:** **$7.0\%$** (Hauler & shovel mechanical outage)
5. **Equipment Fleet Availability:** **$6.8\%$** (Active mining fleet proportion)
6. **Autoregressive Lags (Lag-1 & Rolling 4W):** **$9.3\%$** (Operational momentum)

### 4. Interactive "What-If?" Scenario Simulator
MinePulse allows operations planners to simulate corrective actions before the operating week ends:
- **Downtime Mitigation Slider ($0 - 24\text{ hours}$):** Simulates deploying auxiliary mechanic shifts to repair hydraulic excavators.
- **Blasting Schedule Optimizer ($0 - 12\text{ hours}$):** Simulates clearing pit benches and pre-drilling auxiliary blast patterns during clear weather windows.
- **Dynamic Output:** Computes unadjusted baseline shortfall vs. adjusted recovered tonnage and generates rule-based operational recommendations.

### 5. Automated Operational Shift Advisory
Generates formal, printable DGMS-compliant shift advisories containing:
- Environmental alert status (Pit Flooding Index & Haul Road Degradation Factor).
- Statutory blasting safety compliance (DGMS Section 22 guidelines).
- Tonnage target vs. AI-forecasted shortfall gap.
- Recommended dispatch actions (sump pumping schedules, auxiliary haul truck rerouting).

---

## 💻 Tech Stack & System Requirements

### Backend & Data Science Pipeline
- **Language:** Python 3.10+
- **Machine Learning:** `scikit-learn` (RandomForestRegressor), `xgboost` (XGBRegressor)
- **Data Engineering:** `pandas`, `numpy`
- **APIs & Ingestion:** `requests` (Open-Meteo High-Resolution ERA5 API, NASA POWER Daily API)
- **Spatial Processing:** GeoJSON standard, WGS84 coordinate reference system

### Frontend & User Interface
- **Core:** Semantic HTML5, Vanilla JavaScript (ES6+), Vanilla CSS (Earthy Industrial & Pastel Mining Palette)
- **Geospatial Mapping:** [Leaflet.js 1.9.4](https://leafletjs.com/), [Leaflet.heat Plugin](https://github.com/Leaflet/Leaflet.heat)
- **Cartographic Tiles:** CartoDB DarkMatter & OpenStreetMap
- **Data Visualization:** [Chart.js 4.x](https://www.chartjs.org/)
- **Typography & Icons:** Google Fonts (Outfit & Plus Jakarta Sans), FontAwesome 6.4

---

## 🚀 Getting Started & How to Run

MinePulse is designed with a **zero-dependency, zero-CORS frontend architecture**. The master consolidated dataset is pre-compiled into `data/processed/minepulse_master_data.js`, allowing the complete application to run locally in any web browser without needing a complex Node.js or web server setup.

### Option 1: Quick Launch (Direct in Browser)
1. Clone this repository:
   ```bash
   git clone https://github.com/aniche59/AIML-MDM-Project.git
   cd AIML-MDM-Project
   ```
2. Double-click or open [`index.html`](index.html) directly in any modern web browser (Google Chrome, Firefox, Microsoft Edge, Safari).

### Option 2: Run via Local Python Server (Recommended)
Running through a local web server provides the smoothest experience for live API calls:
```bash
# Launch a lightweight web server on port 8000
python -m http.server 8000
```
Open your browser and navigate to:
```
http://localhost:8000/
```

### Option 3: Retrain ML Models & Refresh Data Pipelines
If you want to re-execute the data science pipeline or retrain the Random Forest and XGBoost models:
1. Install Python dependencies:
   ```bash
   pip install numpy pandas scikit-learn xgboost requests
   ```
2. Run the all-India data pipeline & model trainer:
   ```bash
   python scripts/build_all_india_and_live_pipeline.py
   ```
3. Re-consolidate master dashboard artifacts:
   ```bash
   python scripts/consolidate_dashboard_data.py
   ```

---

## 📂 Repository Directory Structure

```text
AIML-MDM-Project/
├── index.html                                   # Main interactive MinePulse GIS dashboard
├── data_sources.md                              # Formal dataset provenance, citations & math models
├── PROJECT_CONTEXT.md                           # Comprehensive poster & presentation context document
├── README.md                                    # Project documentation (this file)
│
├── context/                                     # Hackathon planning & domain problem documents
│   ├── SIH26009_demo_plan.md                    # Detailed hackathon demo strategy
│   ├── SIH26009_final_implementation_plan.md    # 60-70% prototype execution roadmap
│   └── SIH26009_four_person_work_plan.md        # Modular team division & deliverables
│
├── data/
│   ├── raw/                                     # Unmodified API & catalog downloads
│   │   └── nasa_power_raw_rainfall.json         # Raw NASA POWER meteorological API payload
│   └── processed/                               # Cleaned, standardized & consolidated data
│       ├── all_india_mines.json                 # 12 major Indian manganese mines with geology & reserves
│       ├── gsi_manganese.geojson                # 32 GSI documented deposit occurrences (WGS84)
│       ├── ibm_mine_figures.csv                 # Official IBM Minerals Yearbook 2024 reported figures
│       ├── rainfall_daily.csv                   # Cleaned daily precipitation series (2021-2024)
│       ├── rainfall_weekly.csv                  # 7-day aggregated operational rainfall
│       ├── simulated_operations_weekly.csv      # 208-week operational history (Seed: 26009)
│       ├── forecast_results.csv                 # Holdout comparison (Baseline vs RF vs XGBoost)
│       ├── forecast_metrics.json                # MAE, RMSE, R² scores & feature importance weights
│       ├── sentinel2_context_metadata.json      # Sentinel-2 MSI acquisition & band metadata
│       ├── sentinel2_coverage.geojson           # Satellite overlay spatial extent
│       ├── sentinel2_preview.jpg                # Sentinel-2 true-color reference tile
│       ├── minepulse_master_data.json           # Unified master JSON payload
│       └── minepulse_master_data.js             # Zero-CORS browser-executable master payload
│
├── person 1/                                    # Initial GSI & IBM data extraction workspace
│   ├── Manganese_Ore_deposits_in_India_and_its_salient_features.csv
│   ├── Manganese_Ore_deposits_in_India_and_its_salient_features.geojson
│   ├── ibm_mine_figures (1).csv
│   └── person1_sources_and_limitations (1).md
│
└── scripts/                                     # Automated data engineering & ML training pipelines
    ├── build_all_india_and_live_pipeline.py     # Master ML training, feature engineering & live pipeline
    ├── consolidate_dashboard_data.py            # Bundles all processed assets into master JS/JSON
    ├── fetch_and_process_rainfall.py            # Fetches NASA/IMD daily rainfall & aggregates weekly
    ├── fetch_satellite_image.py                 # Downloads Sentinel-2 imagery preview
    └── prepare_sentinel2_context.py             # Prepares Sentinel-2 bounding box & spectral metadata
```

---

## 🛡️ Academic Integrity & Data Transparency

In compliance with academic evaluation standards and hackathon ethics, MinePulse strictly discloses the origin and limitations of all data:

1. **Public Reference Data (`public_reference`):**
   - *GSI Manganese Occurrences:* Cataloged by Geological Survey of India (last updated 2014). Represents known documented occurrences, **not verified subsurface 3D drill-hole assays or pixel-level reserve ground truth**.
   - *Sentinel-2 MSI Imagery:* 10m optical surface reflectance from ESA Copernicus. Delineates surface alteration and open excavation scars; **does not directly measure underground reserve tonnage**.
2. **Official Reported Figures (`official_reported`):**
   - *IBM Minerals Yearbook 2024:* Reserve and resource figures reported under United Nations Framework Classification (UNFC) by the Indian Bureau of Mines (IBM). Associated with specific mine leases, **not distributed across individual raster cells**.
3. **Simulated Operational Data (`simulated`):**
   - *Weekly Mine Operations (208 weeks):* Detailed daily blasting logs, shovel downtime, and haul truck dispatch records are proprietary to mining companies (such as MOIL). For this prototype, operational features were synthetically generated with realistic mining distributions (Seed: `26009`) coupled to real atmospheric rainfall. Every synthetic chart, table, and CSV is explicitly labelled **`SIMULATED`**.

---

## 👥 Hackathon Team & Roles (SIH26009)

- **Geological & Spatial Data Engineering:** GSI occurrence extraction, IBM Minerals Yearbook standardization, WGS84 GeoJSON conversion.
- **Remote Sensing & Atmospheric Pipeline:** Sentinel-2 multispectral band ratio formulation, NASA POWER/Open-Meteo telemetry ingestion.
- **Machine Learning & Predictive Modeling:** Feature engineering (SFRI, Haul Road Degradation), 80/20 chronological holdout benchmarking (RF vs XGBoost).
- **Dashboard & Full-Stack GIS Development:** Interactive Leaflet geospatial UI, Chart.js time series, What-If simulator, and shift reporting system.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
All external public data sources remain the copyright of their respective agencies (Geological Survey of India, Indian Bureau of Mines, European Space Agency, Open-Meteo, NASA POWER).
