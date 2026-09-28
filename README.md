# 🌾 Igihembwe Alert

District-level crop-yield early warning for Rwanda - NISR 2026 Big Data Hackathon,
Track 1 (Agricultural Productivity).

**Live app:** <add deployed link>  |  **Docs:** [docs/report.md](docs/report.md)

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/make_sample_data.py     # synthetic demo data (replace with real NISR data)
python src/train.py                # trains model, writes predictions + metrics
streamlit run app/app.py
```

## Using real data
Put your merged table in `data/raw/district_season.csv` with columns:
`district, season, rainfall_mm, rainfall_anom, ndvi_mean, temp_mean, yield_t_ha`
(season like `2024A`). Details in [DATA_SOURCES.md](DATA_SOURCES.md).

## Deploy (free)
Streamlit Community Cloud: push to GitHub, choose `app/app.py` as the entry file.
Commit `data/processed/predictions.csv` and `models/metrics.json` so the app
runs without retraining.

## Structure
```
data/ (raw, processed)  src/ (pipeline)  app/ (dashboard)
models/  notebooks/  docs/
```

## Notes
- The bundled data is synthetic - do not present its results as real findings.
- Competition rules: submissions transfer IP to NISR; disclose AI-tool use.
