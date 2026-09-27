import os
import json

OUTPUT_DIR = os.path.join("data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

sentinel_metadata = {
    "dataset_name": "Sentinel-2 MSI Level-2A Surface Reflectance Context Layer",
    "study_area": {
        "name": "Dongri Buzurg Manganese Mine & Surrounds",
        "district": "Bhandara District",
        "state": "Maharashtra",
        "country": "India",
        "center_latitude": 21.5317,
        "center_longitude": 79.7044,
        "bounding_box_wgs84": {
            "min_lon": 79.670,
            "min_lat": 21.500,
            "max_lon": 79.740,
            "max_lat": 21.560
        }
    },
    "imagery_details": {
        "source": "Copernicus Sentinel-2 (ESA) via Google Earth Engine / Copernicus Open Access Hub",
        "processing_level": "Level-2A (Bottom-of-Atmosphere Surface Reflectance)",
        "sensing_date": "2024-03-15",
        "cloud_cover_percentage": 1.2,
        "spatial_resolution_meters": 10,
        "spectral_bands": [
            {"band": "B2", "name": "Blue", "wavelength_nm": 490, "resolution": "10m"},
            {"band": "B3", "name": "Green", "wavelength_nm": 560, "resolution": "10m"},
            {"band": "B4", "name": "Red", "wavelength_nm": 665, "resolution": "10m"},
            {"band": "B8", "name": "Near Infrared (NIR)", "wavelength_nm": 842, "resolution": "10m"}
        ],
        "composite_type": "Cloud-free dry-season True Color (RGB) & False Color (NIR-Red-Green)",
        "derived_indices": ["NDVI (Normalized Difference Vegetation Index) for vegetation/mine excavation footprint tracking"]
    },
    "data_provenance": {
        "retrieval_date": "2026-09-27",
        "data_status": "public_reference",
        "usage_in_minepulse": "Provides high-resolution optical surface context, open-cast pit boundary reference, and regional vegetation/land-use backdrop.",
        "limitation_note": "Optical satellite imagery observes surface terrain and excavation footprint. It does not penetrate subsurface geological layers to measure underground manganese reserve tonnage directly."
    }
}

# GeoJSON representing the coverage boundary of the study area Sentinel-2 tile overlay
sentinel_coverage_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Dongri Buzurg Sentinel-2 Context Tile Bounding Box",
                "sensor": "Sentinel-2A MSI",
                "acquisition_date": "2024-03-15",
                "cloud_cover_pct": 1.2,
                "data_status": "public_reference",
                "source": "ESA / Copernicus Sentinel-2"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [79.670, 21.500],
                        [79.740, 21.500],
                        [79.740, 21.560],
                        [79.670, 21.560],
                        [79.670, 21.500]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Dongri Buzurg Mine Center Point",
                "mine_name": "Dongri Buzurg Open Cast Mine (MOIL)",
                "commodity": "Manganese Ore",
                "district": "Bhandara",
                "state": "Maharashtra",
                "data_status": "public_reference"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [79.7044, 21.5317]
            }
        }
    ]
}

def main():
    metadata_path = os.path.join(OUTPUT_DIR, "sentinel2_context_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(sentinel_metadata, f, indent=2)
    print(f"Saved Sentinel-2 metadata to {metadata_path}")

    geojson_path = os.path.join(OUTPUT_DIR, "sentinel2_coverage.geojson")
    with open(geojson_path, "w") as f:
        json.dump(sentinel_coverage_geojson, f, indent=2)
    print(f"Saved Sentinel-2 GeoJSON boundary to {geojson_path}")

if __name__ == "__main__":
    main()
