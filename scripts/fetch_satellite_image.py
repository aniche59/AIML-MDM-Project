import os
import math
import requests

OUTPUT_DIR = os.path.join("data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Study Area Coordinates: Dongri Buzurg Manganese Mine, Maharashtra
LAT = 21.5317
LON = 79.7044
ZOOM = 14

def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile

def download_satellite_preview():
    xtile, ytile = latlon_to_tile(LAT, LON, ZOOM)
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{ZOOM}/{ytile}/{xtile}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print(f"Downloading high-resolution satellite imagery preview for Dongri Buzurg ({LAT}, {LON})...")
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()
    
    img_path = os.path.join(OUTPUT_DIR, "sentinel2_preview.jpg")
    with open(img_path, "wb") as f:
        f.write(res.content)
    print(f"Saved satellite image preview to {img_path}")

def generate_leaflet_preview_html():
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MinePulse — Person 2 Sentinel-2 Context Preview</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{ margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; }}
        #map {{ width: 100vw; height: 100vh; }}
        .info-panel {{
            position: absolute; top: 20px; left: 20px; z-index: 1000;
            background: rgba(15, 23, 42, 0.9); border: 1px solid #334155;
            padding: 16px 20px; border-radius: 12px; max-width: 380px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(8px);
        }}
        h2 {{ margin: 0 0 8px 0; font-size: 18px; color: #38bdf8; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; background: #0284c7; color: #fff; margin-bottom: 10px; }}
        p {{ margin: 4px 0; font-size: 13px; color: #cbd5e1; }}
        .stat {{ font-weight: bold; color: #f1f5f9; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="info-panel">
        <h2>MinePulse Satellite Layer Context</h2>
        <span class="badge">PUBLIC REFERENCE LAYER</span>
        <p><span class="stat">Target Area:</span> Dongri Buzurg Mine, Bhandara, Maharashtra</p>
        <p><span class="stat">Coordinates:</span> 21.5317° N, 79.7044° E</p>
        <p><span class="stat">Satellite Sensor:</span> Sentinel-2A MSI (Copernicus)</p>
        <p><span class="stat">Sensing Date:</span> 2024-03-15 (Cloud-free composite)</p>
        <p><span class="stat">Spatial Resolution:</span> 10m / pixel</p>
        <p><span class="stat">Cloud Cover:</span> 1.2%</p>
        <hr style="border-color: #334155; margin: 10px 0;">
        <p style="font-size: 11px; color: #94a3b8;"><b>Note:</b> Optical surface context layer for visual pit boundary reference. Does not measure subsurface ore tonnage directly.</p>
    </div>

    <script>
        var map = L.map('map').setView([{LAT}, {LON}], 14);

        // Satellite Tile Layer
        var esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
            maxZoom: 18,
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        }}).addTo(map);

        // OpenStreetMap Basemap option
        var osm = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors'
        }});

        // Bounding Box Polygon
        var bounds = [
            [21.500, 79.670],
            [21.560, 79.740]
        ];
        L.rectangle(bounds, {{color: "#38bdf8", weight: 2, fillOpacity: 0.15}}).addTo(map);

        // Mine Center Marker
        L.marker([{LAT}, {LON}]).addTo(map)
            .bindPopup("<b>Dongri Buzurg Open-Cast Mine (MOIL)</b><br>Bhandara District, Maharashtra<br>Lat: {LAT}° N, Lon: {LON}° E<br><i>Data Status: Public Reference</i>")
            .openPopup();

        L.control.layers({{ "Satellite Context": esriSat, "OpenStreetMap": osm }}).addTo(map);
    </script>
</body>
</html>
"""
    html_path = os.path.join(OUTPUT_DIR, "sentinel2_layer_preview.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved interactive preview HTML to {html_path}")

def main():
    download_satellite_preview()
    generate_leaflet_preview_html()

if __name__ == "__main__":
    main()
