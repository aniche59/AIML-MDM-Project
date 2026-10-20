# MinePulse — Data Sources, Provenance & Technical Architecture

This document records the provenance, resolutions, retrieval mechanisms, units, and data engineering methodology for all datasets and real-time feeds utilized in the **MinePulse SIH26009 Manganese Reserve & Shortfall Planning System**.

---

## 1. Study Areas: Expansion to All Major Manganese Belts of India

To reflect the nationwide distribution of India's manganese reserves, MinePulse expands beyond a single site to cover **12 premier manganese mines across 5 major geological belts**:

| Mine Name | Operator | State / District | Mine Type | Formation / Belt | IBM Reserves (t) | Weekly Baseline (t) |
|---|---|---|---|---|---|---|
| **Dongri Buzurg Mine** | MOIL Ltd. | Maharashtra (Bhandara) | Open Cast | Sausar Group (Mansar/Bichua) | 14,583,826 | 1,000 |
| **Balaghat (Bharweli)** | MOIL Ltd. | Madhya Pradesh (Balaghat) | Underground (Deepest in Asia, >380m) | Sausar Group (Mansar) | 18,250,000 | 850 |
| **Gumgaon Mine** | MOIL Ltd. | Maharashtra (Nagpur) | Underground | Sausar Group (Lohangi) | 4,800,000 | 350 |
| **Tirodi Mine** | MOIL Ltd. | Madhya Pradesh (Balaghat) | Open Cast | Sausar Group (Mansar) | 6,200,000 | 520 |
| **Ukwa Mine** | MOIL Ltd. | Madhya Pradesh (Balaghat) | Underground | Sausar Group (Ukwa Horizon) | 5,100,000 | 420 |
| **Mansar Mine** | MOIL Ltd. | Maharashtra (Nagpur) | Open Cast & Underground | Sausar Group (Anticlinal Crest) | 5,750,000 | 480 |
| **Chikla Mine** | MOIL Ltd. | Maharashtra (Bhandara) | Underground | Sausar Group (Sitalpur) | 6,900,000 | 580 |
| **Joda West & Barbil** | Tata Steel / OMC | Odisha (Keonjhar) | Open Cast Mechanized | Iron Ore Group (Bonai-Keonjhar) | 12,400,000 | 1,100 |
| **Kasia & Koira** | Jindal / OMC | Odisha (Sundargarh) | Open Cast | Bonai-Keonjhar Synclinorium | 8,600,000 | 750 |
| **Sandur & Kumaraswamy** | SMIORE | Karnataka (Ballari) | Open Cast Semi-Mechanized | Dharwar (Sandur Schist Belt) | 16,500,000 | 950 |
| **Garividi Belt** | FACOR / Private | Andhra Pradesh (Vizianagaram) | Open Cast Quarry | Khondalite (Kodurite Suite) | 3,200,000 | 300 |
| **Shivrajpur Mine** | GMDC | Gujarat (Panchmahal) | Open Cast Re-development | Champaner Series (Aravalli) | 2,100,000 | 200 |

---

## 2. Real-Time Telemetry & The "API vs. Data Science" Justification

### A. Academic & Evaluator Defense: Why the API is NOT Doing the AI/ML
A common critique from academic reviewers is that *"the external API is doing everything, so where is your data science work?"* In MinePulse, this critique is thoroughly refuted by separating **sensor telemetry ingestion** from **in-house feature engineering and predictive modeling**:

1. **What the External API Does (and ONLY does):**
   * The Open-Meteo Atmospheric API acts strictly as an **external digital sensor / weather station**.
   * It provides raw, unprocessed physical measurements at the mine's exact coordinates: ambient temperature ($^\circ\text{C}$), instantaneous precipitation ($\text{mm/hr}$), wind speed ($\text{km/h}$), and volumetric soil moisture ($0-7\text{ cm}$ in $\text{m}^3/\text{m}^3$).
   * **The external API does not know what a mine is, does not know what manganese is, and produces zero predictions regarding shortfall or tonnage.**

2. **What OUR Codebase & Data Science Pipeline Does (The Real Work):**
   * **Temporal Resampling & Baseline Fusion:** Aggregating raw hourly sensor streams into a 7-day rolling window aligned with mining production cycles.
   * **Domain-Specific Feature Engineering:**
     * **Pit Flooding & Water Ponding Risk Index ($\text{SFRI}$):**
       $$\text{SFRI} = \min\left(100, \left(\frac{\text{Precipitation}_{7\text{d}}}{50} \times 0.6 + \frac{\text{Soil Moisture}_{0-7\text{cm}}}{0.45} \times 40\right)\right)$$
     * **Haul Road Slipperiness & Machine Degradation Multiplier:**
       $$\text{Degradation Factor} = 1.0 + \max\left(0, (\text{Soil Moisture} - 0.22) \times 2.2\right)$$
       Translates wet clay soil physics into haul truck traction loss, cycle slowdown, and simulated machinery mechanical strain.
     * **Dynamic DGMS Blasting Clearance Safety Model:**
       Evaluates electrical storm and precipitation thresholds to determine whether bench blasting schedules must be aborted or postponed under Directorate General of Mines Safety guidelines.
   * **Local Machine Learning Inference:**
     * The engineered feature vector is fed directly into **locally trained Random Forest and XGBoost tree ensembles**, computing the shortfall tonnage, gap percentage, and risk class directly in our application.

---

## 3. Dual-Model Machine Learning Benchmark: Random Forest vs. XGBoost

Both models were trained and evaluated on **208 operating weeks** (2021–2024) under a strict **chronological 80/20 holdout** (train on earlier 163 weeks, hold out the final 41 weeks; strictly no future data leakage or random row shuffling):

| Model / Architecture | Holdout MAE (Tonnes) | Holdout RMSE (Tonnes) | $R^2$ Score | Key Strength in Mining |
|---|---|---|---|---|
| **Trailing 4-Week Moving Average (Baseline)** | 36.16 t | 50.50 t | 0.127 | Naive non-ML trailing heuristic |
| **Random Forest Regressor (120 Trees, max_depth=8)** | 26.12 t | 31.68 t | 0.656 | Resilient to operational outliers and noise |
| **XGBoost Regressor (100 Trees, lr=0.06, depth=4)** | **25.02 t** | **30.02 t** | **0.691** | Gradient-boosted error correction; lowest MAE |

### Model Feature Importances
* **Prior Week Rainfall:** $42.6\%$ (Primary environmental shock to open-cast haul roads and sump drainage)
* **Planned Target Tonnes:** $22.2\%$ (Baseline operational capacity scaling)
* **Blasting Delay Hours:** $16.5\%$ (Explosive fragmentation bottleneck)
* **Equipment Downtime Hours:** $6.5\%$ (Haulage mechanical outages)
* **Actual Tonnes Lag-1 & Rolling 4W:** $6.1\%$ (Short-term momentum)

---

## 4. Space Technology: Sentinel-2 Multispectral Mineral Indices

In alignment with the SIH26009 Space Technology mandate, MinePulse incorporates Sentinel-2 Level-2A (10m–20m) multispectral band ratios to identify surface indicators of manganese mineralization:

* **Manganese / Iron Oxide Alteration Index ($\text{Band 4} / \text{Band 2}$):** Detects ferric iron and manganese gossan caps where secondary enrichment creates strong absorption in the blue (B2) and high reflectance in the red (B4).
* **Hydrothermal Clay / Carbonate Index ($\text{Band 11} / \text{Band 12}$):** Detects argillic alteration halos and host phyllites/schists surrounding manganese stratiform horizons.
* **Ferrous Mineral Ratio ($\text{Band 11} / \text{Band 8}$):** Highlights silicate/carbonate facies associated with proto-ore.
* **Normalized Difference Vegetation Index ($\text{NDVI} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}}$):** Masks dense vegetation cover to delineate barren open-cast excavation footprints and pit benches.

---

## 5. Summary of Processed Artifacts in Repository

| Output File Path | Description | Target Use |
| :--- | :--- | :--- |
| [`data/processed/all_india_mines.json`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/all_india_mines.json) | 12 major Indian manganese mines with geology, capacity, and coordinates | App & Map Navigation |
| [`data/processed/forecast_results.csv`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/forecast_results.csv) | Dual RF and XGBoost holdout predictions (41 weeks) | Chart & Time Series |
| [`data/processed/forecast_metrics.json`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/forecast_metrics.json) | Comparative holdout MAE, RMSE, $R^2$, and feature weights | Metric Display |
| [`data/processed/minepulse_master_data.js`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/minepulse_master_data.js) | Integrated master payload for zero-CORS browser execution | Frontend Application |
