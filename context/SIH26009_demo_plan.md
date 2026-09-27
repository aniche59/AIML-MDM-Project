# SIH26009: 60–70% Demo Plan

**Problem statement:** Using AI/ML and space technology to identify manganese reserves and reduce production shortfalls  
**Purpose of this document:** A practical build plan for a credible progress presentation. This is a plan and prototype specification; it does not claim the implementation or validation has already been completed.

## 1. The project in one sentence

Build a map-first mine planning prototype that combines public geospatial context with a production shortfall forecast and a transparent “what if?” action panel. The first demo will show how the workflow behaves using public context layers and clearly labelled simulated operations data.

Suggested demo name: **MinePulse**. Keep the Smart India Hackathon problem statement as the formal project title in the presentation.

## 2. Important data reality: this is not fully plug and play

There are useful public datasets, but there is not a ready-made, labelled dataset that supports training a reliable end-to-end model for “manganese reserve tonnes” or MOIL mine shortfalls.

### What is actually available

| Data needed | What we can get | What it supports | Main limitation |
|---|---|---|---|
| Known manganese occurrences | GSI’s Open Government Data catalog has a downloadable spreadsheet of Indian manganese deposit locations and geological descriptions. [Dataset page](https://tn.data.gov.in/catalog/location-manganese-ore-deposits-india-and-its-salient-features) | Plotting documented deposits and showing geological context | The catalog says it was updated in 2014. It is not a current drill-hole database and does not provide a verified label for every map cell, reserve tonnage, depth, or assay grade. |
| Satellite imagery | Sentinel-2 surface reflectance is available in Google Earth Engine from 2017 onward. [Earth Engine catalog](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2) | Basemap imagery, vegetation/land-cover context, and visible surface change | Optical imagery observes the surface. It does not directly establish subsurface manganese reserves. |
| Rainfall and weather | NASA POWER provides daily historical meteorological series. [Daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) | Weather context and a demo weather feature | Its meteorological grid is coarse for a single mine; use it as regional context, not an equipment-level measurement. |
| Soil moisture | NASA SMAP measures global soil moisture. [NASA/JPL mission data](https://podaac.jpl.nasa.gov/SMAP) | Broad wet/dry conditions for context | Satellite soil moisture is not mine-site downtime or a direct measure of whether a particular haul road is usable. |
| Land surface temperature | MODIS MOD11A2 provides an 8-day land-surface-temperature product at 1 km. [Earth Engine catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2) | Regional temperature context | It is too coarse to explain a specific machine failure or blasting delay. |
| MOIL production | MOIL annual reports and press releases disclose aggregate production figures, including periodic monthly/quarterly summaries. [MOIL annual report](https://moil.nic.in/userfiles/Annual_Report_2024_25.pdf), [PIB quarterly summary](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2089799&lang=2&reg=48) | Historical context, public headline totals, and scale checks | These disclosures do not provide the daily mine-by-mine operational history needed to train the proposed shortfall model. |
| Downtime, equipment, blasting and shift logs | No complete public MOIL operational dataset was found in the sources above | These are the features needed for a real operational shortfall model | For the class demo, generate synthetic rows and label them as simulated. For deployment, request approved MOIL data. |

### Are there labelled examples for geology?

There are **known occurrence locations**, which can serve as positive examples. But locations with no recorded occurrence are **unlabelled**, not confirmed barren locations. Treating every other pixel as a negative label would create a misleading training set. Mineral prospectivity research explicitly discusses positive-and-unlabelled learning for this situation, and spatially clustered data needs spatially aware validation. See the [positive-unlabelled prospectivity study](https://doi.org/10.1016/j.cageo.2020.104667) and [spatial validation study](https://doi.org/10.1007/s10618-018-00607-x).

**Decision for this demo:** use the occurrence spreadsheet as map pins/reference context. Do not claim it is enough to train an accurate manganese reserve classifier. If we later obtain suitable geological evidence and enough deposit labels, an experimental positive-unlabelled model can be added, with spatially blocked evaluation and geologist review.

### Are there labelled examples for production?

Public aggregate production totals can be used to describe MOIL’s trend. They are too sparse and lack the operational features (downtime, equipment availability, blasting delays) needed for a credible mine-level supervised forecast. The demo should use a generated operations table. Put a visible **SIMULATED DATA** label on the chart, downloadable CSV, and presentation slide.

## 3. What to reuse from the existing map project

The supplied GitHub link does not resolve in my current browsing context; this plan assumes your team already has access to its own map repo. Keep the map implementation and adapt its data inputs. Do a short repo audit before adding new infrastructure:

1. Identify the current map framework, data format, routing, and layer control.
2. Keep existing basemap, pan/zoom, markers, popups, and layer toggles where they work.
3. Add small adapters that convert data into the format the map already accepts (likely GeoJSON for points/polygons and raster tiles or image overlays for rasters).
4. Add a side panel for forecast, risk, and scenario results. Avoid rebuilding the map or introducing a separate GIS server for the class demo unless the existing app requires it.
5. Record the upstream source, retrieval date, spatial/temporal resolution, and simulated/real status for every layer.

Before copying code or assets from another repository, check its license and preserve its attribution. Since the repo is yours, this is mainly a reminder to retain any third-party license notices included in it.

## 4. Demo scope and completion target

### The 60–70% target means a complete demo workflow

For the progress review, aim to have this end-to-end path working:

**Select a mine area → view public map context → inspect its sample production trend → see a forecast shortfall → inspect the likely drivers → test an operational action → compare the scenario result.**

This is a meaningful 60–70% prototype because the evaluator can follow the system from data to a decision. It does not mean the system has solved reserve estimation or been validated for MOIL operations.

### Must be working for the demo

- Existing interactive map loads reliably.
- Known manganese occurrence points and at least one public satellite/context layer appear on the map.
- Clicking a point/area opens a popup with source, date, and data-status information.
- A mine/area selector drives the charts and forecast panel.
- A clearly labelled simulated production dataset supports the forecast demo.
- The dashboard compares target and forecast output and highlights a shortfall.
- The app names the largest modelled risk drivers.
- At least two “what if?” actions update the scenario output.
- The screen and slides distinguish observations, model outputs, and assumptions.

### Can remain a roadmap item

- MOIL drill-hole, assay, grade-control, geophysical, and surveyed reserve integration.
- Real mine-by-mine equipment telemetry and maintenance logs.
- A validated manganese prospectivity ML model.
- Automatic live satellite processing and alert delivery.
- Mine scheduling optimisation against real shift, safety, and capacity constraints.
- Production deployment, authentication, and integration with MOIL systems.

## 5. Recommended algorithms

### A. Production shortfall forecast: baseline first, Random Forest second

Do not start with an LSTM or a complicated deep-learning model. You do not have a long, clean, mine-level time series, and a deep model trained on generated rows would look impressive but be hard to defend.

Use two outputs in the prototype:

1. **Baseline:** forecast the next period using recent average production (for example, the trailing 4-period average) or a seasonal-naive value if the sample data has a repeated seasonal pattern.
2. **ML demo model:** `RandomForestRegressor` predicting next-period tonnes from simulated operations features. It handles nonlinear interactions, works with mixed operational feature scales, and is straightforward to explain with permutation importance.

Suggested target and features:

| Kind | Column | Meaning |
|---|---|---|
| Target | `actual_tonnes_next_period` | Simulated tonnes produced in the next day/week/month, matching the chosen demo period |
| Plan | `planned_tonnes` | Production target for that period |
| Equipment | `equipment_available_pct`, `downtime_hours`, `critical_units_down` | Simulated machine availability and outages |
| Weather | `rainfall_mm`, `soil_moisture_index` | Public or simulated weather/context input; use a clear source/resolution label if public |
| Blasting | `blast_delay_hours`, `blasts_planned`, `blasts_completed` | Simulated blasting status |
| Recent history | `actual_tonnes_prev_1`, `actual_tonnes_prev_2`, `rolling_mean_4` | Lagged production values |
| Context | `mine_id`, `mine_type`, `period` | Mine and time information; do not leak future data into features |

The dashboard computes:

- `forecast_gap_tonnes = planned_tonnes - forecast_tonnes`
- `shortfall_pct = max(0, forecast_gap_tonnes / planned_tonnes * 100)`
- risk band based on a documented threshold (for example: low below 5%, medium 5–10%, high above 10%). These thresholds are prototype settings, not MOIL policy.

**Evaluation:** use a chronological holdout (train on earlier periods, score later periods). Report MAE and a chart of predicted versus simulated actual tonnes. Compare the Random Forest with the baseline. Do not use a random row split for a time series. Do not quote impressive accuracy unless the holdout result supports it.

**Truthful wording:** “The forecast model demonstrates the workflow using simulated operations records. It has not been validated against MOIL’s mine-level operational data.”

### B. Risk driver explanation: simple contribution logic, not a causal claim

Use permutation importance for a global “which fields mattered to the model?” view. For an individual forecast, use a transparent local rule panel that compares the selected scenario inputs with the normal scenario (for example, availability is 18 points below the configured reference, and rainfall is above the configured threshold).

Avoid saying “rain caused this shortfall” unless a causal analysis supports it. Say “the model flags low equipment availability as a major contributor in this simulated case.”

### C. Corrective actions: scenario calculator, not an optimiser yet

Create three explicit, editable scenario rules:

| Action | User control | Scenario calculation |
|---|---|---|
| Redeploy equipment | Increase available equipment or reduce downtime by a chosen amount | Re-run the forecast with the modified availability/downtime fields |
| Reschedule blasting | Reduce the simulated blast delay or move a blast to an available slot | Re-run the forecast with the adjusted delay/completion fields |
| Weather-aware schedule | Select a dry-window assumption or reduce weather exposure | Re-run using the chosen weather assumption; label it an assumption |

Show base forecast, changed inputs, scenario forecast, and tonnes recovered in adjacent cards. Add a note: **“Scenario result is a modelled estimate from prototype assumptions; it is not a guaranteed operational recovery.”**

### D. Geological map: use GIS scoring for this demo, not a fake supervised classifier

For the first release, present a **geological/satellite context map**. If a visible score is needed, use a clearly documented, expert-set **screening score** from available map layers (such as proximity to documented occurrences and presence of a supplied permissive geological unit). Show the component layers and weights. Call it “screening score” or “context score,” not probability of ore or reserve estimate.

Only add a learned prospectivity model if there are enough trustworthy training labels and geological predictor layers. In that later experiment:

- Use known occurrences as positive samples and background pixels as unlabelled, rather than treating all background as verified negative.
- A positive-unlabelled bagging model or PU Random Forest is a reasonable first experiment; compare its maps across multiple background samples.
- Hold out spatial blocks or entire occurrence clusters. Randomly splitting nearby pixels can overstate performance because spatially neighbouring samples are similar.
- Keep the map inside the range of geology represented by training data and show uncertainty/unsupported areas.
- Validate with a geologist and, ultimately, independent drilling or field evidence before claiming reserve identification.

## 6. Data preparation plan

### Public geospatial context

1. Download the GSI manganese occurrence spreadsheet.
2. Preserve the raw file unchanged in a `data/raw/` folder.
3. Convert usable coordinates into the map’s point format (GeoJSON or its existing equivalent).
4. Include fields such as `name`, `state`, `host_rock`, `formation`, `source_url`, `source_year`, and `data_status: public_reference`.
5. Select a small area relevant to the intended demo. Do not plot every national point if it makes the map unreadable.
6. Add Sentinel-2 imagery/context only if the current map can display it without a major rewrite. Start with a static exported image or tile layer if live Earth Engine integration will consume too much time.
7. Add rainfall/temperature/soil moisture as contextual summaries with their resolution and time window visible. These explain environmental context, not ore occurrence.

### Simulated operations table

Generate a CSV with a few hundred daily or weekly rows across 2–4 fictional mine areas. Each row should be internally consistent: a period with more equipment downtime and blast delay should usually have lower actual output, while retaining some noise. Keep all fictional mine names clearly marked as demo sites; do not make simulated rows appear to be MOIL records.

Suggested columns:

```text
period_start,mine_id,planned_tonnes,actual_tonnes,
equipment_available_pct,downtime_hours,critical_units_down,
rainfall_mm,soil_moisture_index,blast_delay_hours,
blasts_planned,blasts_completed,shift_count,data_status
```

Create a short `data/README.md` or in-app “Data & assumptions” view recording the source or generation method for each column.

### Public production context

Use MOIL reports only for aggregate historical context and for checking the order of magnitude of charts. If transcribing values from a report, store the report URL, reporting period, units, and whether values are provisional. Do not combine annual aggregate production with simulated daily mine rows as if they were one continuous dataset.

## 7. Suggested app structure (adapt to the existing repo)

Keep the current frontend and map. Add only the parts needed for this demo:

```text
existing-map-app/
  data/
    raw/                 # downloaded public files; no edits to source files
    processed/           # cleaned GeoJSON/CSV used by the app
    demo/                # simulated operations CSV, clearly labelled
    README.md            # provenance, units, dates, assumptions
  src-or-app/
    data_adapter         # load/validate CSV and geospatial features
    forecast             # baseline and Random Forest prediction
    scenarios            # transparent action assumptions and recalculation
    map_layers           # adapt existing map layer inputs
    dashboard           # forecast cards, charts, data status labels
```

This is a logical layout, not a requirement to restructure the current repository. Fit the pieces into the code already there.

## 8. Dashboard screens and what each should show

### Screen 1: Overview map

- Existing basemap and zoom controls.
- Public manganese occurrence points, with distinguishable symbols.
- Optional geology boundary or Sentinel-2 context layer if sourced and prepared.
- Mine/demo-area selector.
- Layer legend with source and date.
- Map popup: occurrence name, location, geological description if present, dataset source/year, and a note that the point is a documented occurrence rather than a verified current reserve.

### Screen 2: Production outlook

- Planned versus actual historical production chart.
- Next-period forecast and forecast horizon.
- Shortfall tonnage and shortfall percentage.
- Risk band with threshold shown.
- Baseline model comparison and evaluation metric from the chronological holdout.
- Persistent `SIMULATED DEMO DATA` badge.

### Screen 3: Drivers and actions

- Three leading modelled risk drivers.
- Input controls for equipment uptime/downtime, blast delay, and weather assumption.
- Base forecast versus scenario forecast.
- Expected tonnes recovered in the scenario.
- Assumptions and limitation note.

### Screen 4: Data and method (can be a tab or modal)

- Dataset name, source link, date retrieved, spatial/temporal resolution, status (public, simulated, future integration).
- Forecast algorithm and evaluation approach.
- Plain-language explanation of why the map does not claim subsurface reserve quantities.

## 9. One-week build sequence (compress or stretch to your class date)

### Day 1 — Audit and freeze scope

- Run the existing map locally; capture the current working features.
- Check the repo license and dependency setup.
- Choose one demo area and one forecasting period (weekly is easiest to narrate).
- Make a list of every real, public, and simulated field.
- Agree that the demo makes no real reserve-tonnage claim.

**Exit check:** team can state the demo story in one sentence; app runs unchanged.

### Day 2 — Prepare public map context

- Download and inspect the GSI occurrence spreadsheet.
- Convert the selected rows to the map’s format.
- Add provenance fields and popups.
- Add one satellite/context layer if straightforward.

**Exit check:** map shows a sourced layer and point popup; no unexplained markers.

### Day 3 — Build the simulated operations data and baseline

- Generate and document the operations CSV.
- Add the planned-versus-actual chart and trailing-average baseline forecast.
- Add target, tonnes gap, and risk thresholds.

**Exit check:** selecting a demo area changes the chart and baseline forecast.

### Day 4 — Add and evaluate Random Forest prototype

- Train the regressor using past simulated periods only.
- Use a chronological train/holdout split.
- Compare MAE with the simple baseline.
- Add permutation importance or simple input comparison for risk drivers.

**Exit check:** model score and method are visible; the metric is reproducible from the checked-in data.

### Day 5 — Add recommendation scenarios and map linkage

- Add redeployment and blast-delay controls.
- Recalculate forecast when controls change.
- Link the selected site to its map marker and production panel.

**Exit check:** user can select a site, see the shortfall, and show at least two changed scenarios.

### Day 6 — Polish and presentation rehearsal

- Add `SIMULATED`, source, date, unit, and limitation labels.
- Test the full demo path on the presentation laptop/browser.
- Prepare screenshots/video fallback and a fixed demo CSV.
- Rehearse likely questions and make sure each team member explains their part consistently.

**Exit check:** a 3-minute demo can run without editing code or explaining away missing data.

## 10. Four-person team split

| Role | Owns | Deliverable |
|---|---|---|
| Map and integration | Existing repo audit, data adapters, map layers and popups | Working map with sourced context layers |
| Data and GIS | GSI spreadsheet, coordinate cleanup, satellite/weather layer selection, provenance | Processed spatial data and data dictionary |
| ML and operations | Simulated production data, baseline, Random Forest, holdout evaluation, driver display | Forecast and model comparison |
| UI and presentation | Dashboard flow, scenario controls, limitations, slides and rehearsal | Clear end-to-end story and Q&A readiness |

Have one person own integration and merges. Agree on column names and GeoJSON fields on Day 1 so the map and model don’t create incompatible data formats.

## 11. Demo script (about 3 minutes)

1. **Problem (20 seconds):** “Planning can be affected by production shortfalls. We built a prototype that connects spatial context with a production planning view.”
2. **Map (35 seconds):** select a demo area; show the occurrence points and satellite/context layer; open a popup showing the source and year.
3. **Data honesty (15 seconds):** “Public occurrence and satellite layers are real. Operations logs are not publicly available at the required granularity, so the planning demonstration uses explicitly simulated records.”
4. **Forecast (45 seconds):** show historical simulated output, target, baseline, Random Forest forecast, holdout metric, and shortfall risk.
5. **Drivers (25 seconds):** show the modelled inputs associated with the forecast; explain that they are associations in the prototype, not proven causes.
6. **Action scenario (40 seconds):** change downtime or blast delay; show changed forecast and recovered tonnes under the scenario assumptions.
7. **Boundary and next step (20 seconds):** “The map is exploration context, not a reserve estimate. With MOIL drill and operations data, we would validate and retrain the models before operational use.”

## 12. Presentation slide outline

1. Title, SIH problem statement, team.
2. Current pain points and intended users.
3. Data availability: public context versus data needed from MOIL.
4. System flow: map/data → forecast → risk explanation → scenario action.
5. Architecture and what is reused from the current map project.
6. Working map screenshots with source labels.
7. Forecast method, baseline comparison, and simulated-data evaluation.
8. Action scenario: before/after forecast and assumptions.
9. What is implemented for this checkpoint (target 60–70%) and what is next.
10. Limitations, validation plan, and specific data partnership request.

## 13. Questions evaluators may ask

**“Is your dataset labelled?”**  
“The public GSI catalog gives documented occurrence locations, so we have positive/reference points. It does not provide verified barren-area labels or reserve tonnes. Our first map uses the points as context; we are not claiming a validated reserve classifier.”

**“Are these MOIL production predictions?”**  
“No. The operational records in this demo are simulated because mine-level target, downtime, equipment, and blasting data were not found in the public sources we checked. The forecast demonstrates the pipeline and must be retrained and validated with MOIL data.”

**“Why use satellite data if it cannot see underground ore?”**  
“Satellite data provides surface and environmental context. It can support monitoring and help prioritize review when combined with geological evidence. It does not replace geological surveys, drill logs, or reserve estimation.”

**“Why Random Forest?”**  
“It is a practical tabular-data baseline for nonlinear interactions and is easy to compare with a simple moving-average forecast. We use a time-ordered holdout and keep the model small and interpretable. The demo result is not a claim of deployment accuracy.”

**“How will you validate reserve potential?”**  
“With independent geological evidence such as drill intersections, assays and geophysical/geological layers, spatially separated evaluation, geologist review, and ultimately field or drilling confirmation. Those data are outside this public-data prototype.”

## 14. Risks and guardrails

- **False reserve claim:** never display “estimated manganese tonnes” from surface/weather layers. Use occurrence markers or screening context.
- **Synthetic data presented as real:** show a persistent badge, label files, and disclose it in the first minute of the demo.
- **Random split inflates model score:** keep later periods in the holdout; for geology, hold out spatial blocks/clusters.
- **Public aggregate production mistaken for mine-level history:** keep official totals in a separate context chart from simulated operational records.
- **Unclear provenance:** every layer needs a source, date, units, and resolution.
- **Too much scope:** prioritize the complete planning workflow over a half-finished advanced satellite classifier.

## 15. Definition of “ready to present”

The progress presentation is ready when:

- [ ] Existing map launches from a clean start.
- [ ] At least one real public reference layer is visible and cited in the app.
- [ ] Every demo operations record is marked simulated.
- [ ] Baseline and ML forecast can be compared on a chronological holdout.
- [ ] The dashboard shows target, forecast, gap, risk threshold, and units.
- [ ] Two scenario controls visibly change the forecast.
- [ ] One person can run the full story in three minutes.
- [ ] Slides explain what the app does, what data is missing, and what would validate the claims.
- [ ] Nobody describes the current map score as a verified reserve or the sample forecast as MOIL’s actual output.

## 16. Sources

- [GSI manganese deposits catalog, Open Government Data Platform India](https://tn.data.gov.in/catalog/location-manganese-ore-deposits-india-and-its-salient-features)
- [Sentinel-2 data catalog, Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2)
- [NASA POWER daily API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)
- [NASA SMAP data portal](https://podaac.jpl.nasa.gov/SMAP)
- [MODIS MOD11A2 land surface temperature catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A2)
- [MOIL Annual Report 2024–25](https://moil.nic.in/userfiles/Annual_Report_2024_25.pdf)
- [Press Information Bureau MOIL quarterly production summary](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2089799&lang=2&reg=48)
- [Positive and unlabelled learning for mineral prospectivity mapping](https://doi.org/10.1016/j.cageo.2020.104667)
- [Spatial leave-pair-out validation for spatial classifiers](https://doi.org/10.1007/s10618-018-00607-x)
