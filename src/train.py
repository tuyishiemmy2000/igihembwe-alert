"""Train, evaluate (time-based split) and export district risk scores."""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score

from features import FEATURES, TARGET, build_features

RAW = Path("data/raw/district_season.csv")
OUT_PRED = Path("data/processed/predictions.csv")
OUT_MODEL = Path("models/model.joblib")
OUT_METRICS = Path("models/metrics.json")


def risk_level(drop_pct: float) -> str:
    if drop_pct >= 15:
        return "High"
    if drop_pct >= 5:
        return "Medium"
    return "Low"


def main(n_test_seasons: int = 4):
    df = build_features(pd.read_csv(RAW))
    seasons = sorted(df["season"].unique(), key=lambda s: (int(s[:4]), s[4]))
    test_seasons = seasons[-n_test_seasons:]
    train, test = df[~df.season.isin(test_seasons)], df[df.season.isin(test_seasons)]

    model = RandomForestRegressor(n_estimators=300, min_samples_leaf=2,
                                  random_state=42, n_jobs=-1)
    model.fit(train[FEATURES], train[TARGET])
    pred = model.predict(test[FEATURES])

    baseline = test["lag1_yield"]  # naive: same as last season
    metrics = {
        "test_seasons": test_seasons,
        "model_MAE": round(float(mean_absolute_error(test[TARGET], pred)), 4),
        "model_R2": round(float(r2_score(test[TARGET], pred)), 4),
        "naive_MAE": round(float(mean_absolute_error(test[TARGET], baseline)), 4),
        "naive_R2": round(float(r2_score(test[TARGET], baseline)), 4),
    }
    imp = permutation_importance(model, test[FEATURES], test[TARGET],
                                 n_repeats=10, random_state=42)
    metrics["feature_importance"] = {
        f: round(float(v), 4) for f, v in
        sorted(zip(FEATURES, imp.importances_mean), key=lambda x: -x[1])
    }

    # Risk = predicted yield vs the district's own historical mean (train period)
    hist_mean = train.groupby("district")[TARGET].mean()
    out = test[["district", "season", TARGET] + FEATURES[:3]].copy()
    out["predicted_yield"] = pred.round(3)
    out["hist_mean_yield"] = out["district"].map(hist_mean).round(3)
    out["drop_pct"] = ((out.hist_mean_yield - out.predicted_yield)
                       / out.hist_mean_yield * 100).round(1)
    out["risk"] = out["drop_pct"].map(risk_level)

    for p in (OUT_PRED, OUT_MODEL, OUT_METRICS):
        p.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PRED, index=False)
    joblib.dump(model, OUT_MODEL)
    OUT_METRICS.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
