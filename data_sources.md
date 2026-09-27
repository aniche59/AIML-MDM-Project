# MinePulse — Data Sources & Provenance Metadata

This document records the provenance, resolution, retrieval dates, units, and data status for all Person 2 datasets (Satellite & Weather context) for the SIH26009 Manganese Planning prototype.

---

## 1. Selected Study Area

* **Mine / District:** Dongri Buzurg Manganese Mine (MOIL), Bhandara District, Maharashtra, India
* **Center Coordinates:** `Latitude: 21.5317° N`, `Longitude: 79.7044° E`
* **Geographic Extent:** `[79.670° E, 21.500° N]` to `[79.740° E, 21.560° N]`
* **Rationale:** Dongri Buzurg is MOIL’s premier open-cast manganese mine in Maharashtra, located within the Nagpur-Bhandara manganese belt.

---

## 2. Rain & Meteorological Data

### A. Daily Gridded Rainfall (`data/processed/rainfall_daily.csv`)
* **Source:** NASA POWER AG Daily API (Agroclimatology) / IMD Gridded Reference Fallback
* **Parameter:** `PRECTOTCORR` (Corrected Total Precipitation in mm/day)
* **Spatial Resolution:** 0.5° × 0.5° regional meteorological grid (~50 km)
* **Coverage Period:** January 1, 2021 – December 31, 2024 (1,461 daily rows)
* **Units:** Millimeters (`mm`)
* **Data Status Tag:** `public_reference`
* **Limitation Note:** This is regional gridded rainfall interpolated from satellite and meteorological reanalysis models. It provides environmental context for rainfall exposure, but is **not** an on-site mine rain gauge measurement.

### B. Weekly Aggregated Rainfall (`data/processed/rainfall_weekly.csv`)
* **Source:** Derived by summing `rainfall_daily.csv` into 7-day operating weeks (starting Monday).
* **Coverage:** 208 complete operating weeks (2021 – 2024).
* **Fields:** `week_start`, `mine_id`, `location`, `latitude`, `longitude`, `rainfall_mm`, `max_daily_rainfall_mm`, `data_source`, `data_status`.
* **Units:** Millimeters (`mm`) per week.
* **Hand-Off:** Passed directly to **Person 3** for training the `RandomForestRegressor` and generating realistic weekly operational rows.

---

## 3. Satellite Context Layer (`data/processed/sentinel2_context_metadata.json` & `sentinel2_coverage.geojson`)

* **Source:** ESA Copernicus Sentinel-2 MSI Level-2A (Surface Reflectance) via Google Earth Engine catalog
* **Acquisition Date:** March 15, 2024 (Cloud-free dry season composite)
* **Cloud Cover:** 1.2%
* **Spatial Resolution:** 10 meters per pixel (Bands B2, B3, B4, B8)
* **Spectral Bands Used:** True Color RGB (B4, B3, B2) & False Color / NDVI (B8, B4)
* **Data Status Tag:** `public_reference`
* **Usage in App:** Displays open-cast pit surface context, vegetation footprint, and mine extent overlay on the interactive dashboard map.
* **Limitation Note:** Optical surface reflectance measures surface terrain, land cover, and visible excavation footprints. **It does not directly observe underground manganese reserve tonnage or grade.**

---

## 4. Summary of Output Files Created for Person 3 & Person 4

| Output File Path | Description | Target User |
| :--- | :--- | :--- |
| [`data/processed/rainfall_daily.csv`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/rainfall_daily.csv) | 1,461 daily rainfall rows (2021–2024) | Person 3 & 4 |
| [`data/processed/rainfall_weekly.csv`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/rainfall_weekly.csv) | 208 weekly aggregated rainfall totals | **Person 3 (ML Training)** |
| [`data/processed/sentinel2_context_metadata.json`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/sentinel2_context_metadata.json) | Sentinel-2 acquisition & provenance details | **Person 4 (Dashboard)** |
| [`data/processed/sentinel2_coverage.geojson`](file:///c:/Users/temp/Desktop/College/MDM/data/processed/sentinel2_coverage.geojson) | GeoJSON bounding box & center point feature | **Person 4 (Map Layer)** |
