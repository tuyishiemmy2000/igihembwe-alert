# Data sources

| Data | Source | Use |
|---|---|---|
| Crop area and yield by district and season | NISR Seasonal Agriculture Survey (SAS) - statistics.gov.rw | Target variable (yield_t_ha) |
| Household food security / poverty context | NISR EICV, CFSVA | Context, prioritisation |
| Rainfall | CHIRPS (open) | rainfall_mm, rainfall_anom |
| Vegetation index | Sentinel-2 / MODIS NDVI (open) | ndvi_mean |
| Temperature | NASA POWER (open) | temp_mean |

Verify exact dataset names, versions and licences on the NISR data portal before use.

**The repo ships a synthetic generator** (`src/make_sample_data.py`) so the pipeline
runs anywhere. Replace `data/raw/district_season.csv` with the real merged table
(same columns) and re-run `python src/train.py`.
