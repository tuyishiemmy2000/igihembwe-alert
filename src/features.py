import pandas as pd

FEATURES = ["rainfall_anom", "ndvi_mean", "temp_mean", "lag1_yield",
            "lag2_yield", "is_season_A", "district_code"]
TARGET = "yield_t_ha"


def season_order(s: str) -> float:
    return int(s[:4]) + (0.0 if s.endswith("A") else 0.5)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["t"] = df["season"].map(season_order)
    df = df.sort_values(["district", "t"]).reset_index(drop=True)
    g = df.groupby("district")[TARGET]
    df["lag1_yield"] = g.shift(1)
    df["lag2_yield"] = g.shift(2)
    df["is_season_A"] = df["season"].str.endswith("A").astype(int)
    df["district_code"] = df["district"].astype("category").cat.codes
    return df.dropna(subset=["lag1_yield", "lag2_yield"]).reset_index(drop=True)
