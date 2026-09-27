# Person 1 — GSI + IBM Data Note

## Demo area
Dongri Buzurg Manganese Mine, Tumsar Tehsil, Bhandara District, Maharashtra.

## GSI source
Official dataset: "Location of Manganese Ore Deposits in India and its Salient Features"
Provider: Ministry of Mines, Geological Survey of India, OGD Platform India.
The uploaded working copy is an ArcGIS/SelectDataset mirror of the GSI/OGD dataset. The mirror states that source attributes are intact and that decimal-degree coordinates were added.

## GSI processing
- Raw file: Manganese_Ore_deposits_in_India_and_its_salient_features.csv
- Input rows: 32
- Output rows: 32
- Exact duplicate rows removed: 0
- Duplicate coordinate rows removed: 0
- Invalid India-coordinate rows removed: 0
- Standardized state names: Maharastra -> Maharashtra; Chattisgarh -> Chhattisgarh; Orissa -> Odisha.
- Coordinates used: latdd/londd decimal degrees.
- CRS: WGS84 / EPSG:4326.
- Data status: documented_occurrence.

## Important Dongri Buzurg finding
The 32-row GSI working copy does NOT contain a locality named "Dongri Buzurg" or an exact Dongri Buzurg coordinate. Therefore no Dongri Buzurg point was fabricated or inserted into the GSI occurrence layer. The dashboard can use the separately sourced demo-area center from the team's satellite/context layer.

## IBM figure
IBM Indian Minerals Yearbook 2024, Table 2, page 66 (PDF page 80), lists Dongri Buzurg Mine, For Lease 174.80 Ha., Tumsar Tehsil, Bhandara District, Maharashtra and reports in-situ ore reserves & resources as of 31.03.2024 under UNFC classification. The classification figures and IBM's reported total are preserved exactly in ibm_mine_figures.csv.

## QA note
The seven classification figures printed by IBM sum arithmetically to 12,568,876 tonnes, whereas IBM's printed total is 14,583,826 tonnes. The CSV therefore preserves IBM's stated total rather than silently recalculating it. This discrepancy should be mentioned if the figure is displayed in the demo.

## Limitation
GSI occurrence points are historical/documented geological occurrences from the source dataset. They should not be described as newly verified reserves. IBM's mine figure is an official reported reserve/resource figure for the named Dongri Buzurg mine and date.
