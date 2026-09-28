# Igihembwe Alert - Project Documentation

## 1. Problem and relevance
Seasonal yield swings driven by rainfall variability hit smallholder farmers hard,
yet district planners often react after the season is lost. Igihembwe Alert
predicts district-level yield risk before harvest. Aligned with NST2 agricultural
transformation priorities and Vision 2050 food-security goals.
Users: district agronomists, MINAGRI planners, cooperatives, NGOs.

## 2. Data
See DATA_SOURCES.md. Unit of analysis: district x season (A/B), 30 districts.
Cleaning: standardise district names, align seasons, check outliers, impute
missing climate values with district-season medians.

## 3. Methodology
- Features: rainfall anomaly, NDVI, temperature, lagged yield (1 and 2 seasons),
  season type, district.
- Model: Random Forest regressor (baseline: last season's yield).
- Validation: time-based split - last 4 seasons held out (no leakage).
- Risk rule: predicted yield vs district historical mean;
  drop >= 15% = High, 5-15% = Medium, otherwise Low.
- Explainability: permutation importance.
- Results: see `models/metrics.json` after running `src/train.py`
  (record final numbers here).

## 4. System
data/raw -> src/features.py -> src/train.py -> predictions.csv + model.joblib
-> app/app.py (Streamlit dashboard: risk bars, district advice, CSV download).

## 5. Impact and sustainability
Earlier warning for targeted irrigation, storage and extension support.
Can be re-run each season as new SAS and climate data are released; extendable to
maps (district GeoJSON), Kinyarwanda alerts and SMS delivery.

## 6. Limitations
Small sample per district; district averages hide within-district variation;
predictions depend on quality of survey and satellite data.

## 7. Team, AI-use disclosure and references
Team: <name 1> (Rwandan citizen), <name 2>.
AI use: <declare tools used and for what - required by the competition rules>.
References: NISR SAS; CHIRPS; NASA POWER; Sentinel-2.
