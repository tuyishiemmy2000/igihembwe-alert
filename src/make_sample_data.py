"""Generate a SYNTHETIC district-season dataset so the pipeline runs end to end.

!! Replace with real data !!
Put your real merged table at data/raw/district_season.csv with the same columns:
district, season, rainfall_mm, rainfall_anom, ndvi_mean, temp_mean, yield_t_ha
(yield from NISR Seasonal Agriculture Survey; rainfall from CHIRPS; NDVI from
Sentinel-2/MODIS; temperature from NASA POWER). See DATA_SOURCES.md.
"""
import numpy as np
import pandas as pd
from pathlib import Path

DISTRICTS = [
    "Nyarugenge", "Gasabo", "Kicukiro", "Nyanza", "Gisagara", "Nyaruguru",
    "Huye", "Nyamagabe", "Ruhango", "Muhanga", "Kamonyi", "Karongi",
    "Rutsiro", "Rubavu", "Nyabihu", "Ngororero", "Rusizi", "Nyamasheke",
    "Rulindo", "Gakenke", "Musanze", "Burera", "Gicumbi", "Rwamagana",
    "Nyagatare", "Gatsibo", "Kayonza", "Kirehe", "Ngoma", "Bugesera",
]
SEASONS = [f"{y}{s}" for y in range(2015, 2026) for s in ("A", "B")]


def main(out="data/raw/district_season.csv", seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    base = {d: rng.uniform(1.6, 3.2) for d in DISTRICTS}
    dry_prone = {"Bugesera", "Nyagatare", "Kirehe", "Kayonza", "Ngoma", "Gatsibo"}
    for d in DISTRICTS:
        for s in SEASONS:
            mean_rain = 450 if s.endswith("A") else 300
            if d in dry_prone:
                mean_rain *= 0.75
            rain = max(40, rng.normal(mean_rain, 0.25 * mean_rain))
            anom = (rain - mean_rain) / (0.25 * mean_rain)
            ndvi = np.clip(0.55 + 0.08 * anom + rng.normal(0, 0.04), 0.2, 0.9)
            temp = rng.normal(20.5 if d not in dry_prone else 22.5, 0.8)
            y = base[d] * (1 + 0.14 * anom + 0.9 * (ndvi - 0.55) - 0.03 * (temp - 21))
            y *= rng.normal(1, 0.05)
            rows.append((d, s, round(rain, 1), round(anom, 3), round(ndvi, 3),
                         round(temp, 2), round(max(0.3, y), 3)))
    df = pd.DataFrame(rows, columns=["district", "season", "rainfall_mm",
                                     "rainfall_anom", "ndvi_mean", "temp_mean",
                                     "yield_t_ha"])
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} rows to {out} (SYNTHETIC - replace with real data)")


if __name__ == "__main__":
    main()
