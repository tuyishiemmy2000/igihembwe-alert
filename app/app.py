"""Igihembwe Alert - district crop-yield risk dashboard (Streamlit)."""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Igihembwe Alert", page_icon="🌾", layout="wide")

ADVICE = {
    "High": "Prioritise small-scale irrigation and drought-tolerant seed; "
            "pre-position post-harvest storage and extension visits.",
    "Medium": "Monitor rainfall weekly; promote soil moisture conservation "
              "(mulching, terraces) and early planting advice.",
    "Low": "Normal support. Focus on post-harvest handling and market linkage.",
}
COLORS = {"High": "#d62728", "Medium": "#ff9f1c", "Low": "#2ca02c"}


@st.cache_data
def load():
    pred = pd.read_csv(ROOT / "data/processed/predictions.csv")
    metrics = json.loads((ROOT / "models/metrics.json").read_text())
    return pred, metrics


try:
    pred, metrics = load()
except FileNotFoundError:
    st.error("Run the pipeline first: python src/make_sample_data.py && python src/train.py")
    st.stop()

st.title("🌾 Igihembwe Alert")
st.caption("Seasonal crop-yield early warning for Rwanda's districts "
           "(demo uses synthetic data unless real NISR data is provided).")

season = st.sidebar.selectbox("Season", sorted(pred.season.unique(), reverse=True))
level = st.sidebar.multiselect("Risk level", ["High", "Medium", "Low"],
                               default=["High", "Medium", "Low"])
in_season = pred[pred.season == season]
view = in_season[in_season.risk.isin(level)].sort_values("drop_pct", ascending=False)

c1, c2, c3, c4 = st.columns(4)
c1.metric("High-risk districts", int((in_season.risk == "High").sum()))
c2.metric("Medium-risk districts", int((in_season.risk == "Medium").sum()))
c3.metric("Model MAE (t/ha)", metrics["model_MAE"])
c4.metric("Model R²", metrics["model_R2"])

fig = px.bar(view, x="drop_pct", y="district", color="risk", orientation="h",
             color_discrete_map=COLORS,
             labels={"drop_pct": "Predicted yield drop vs district average (%)",
                     "district": ""}, height=750)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("What to do in a district")
options = view.district.tolist() or in_season.district.tolist()
d = st.selectbox("District", options)
row = in_season[in_season.district == d].iloc[0]
st.markdown(f"**{d} - {season}: {row.risk} risk** "
            f"(predicted {row.predicted_yield} t/ha vs average {row.hist_mean_yield} t/ha)")
st.info(ADVICE[row.risk])

with st.expander("Why? Main drivers (permutation importance)"):
    st.bar_chart(pd.Series(metrics["feature_importance"]))

st.download_button("Download table (CSV)", view.to_csv(index=False), "risk_table.csv")
