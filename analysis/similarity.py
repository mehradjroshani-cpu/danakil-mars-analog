"""Approximate analog-similarity index: Danakil Depression vs Meridiani Planum (Mars).

Median slope comes from the DEM notebook (data/results.csv). The other physical inputs
are APPROXIMATE literature-style values in data/approx_values.csv.
Mineralogy/aqueous scores are expert-judgement placeholders, to be replaced with
ASTER band-ratio vs CRISM comparisons. Replace values with computed ones before submitting.
"""
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # works from any working directory
DATA, FIGS = os.path.join(ROOT, "data"), os.path.join(ROOT, "figures")
os.makedirs(FIGS, exist_ok=True)

d = pd.read_csv(os.path.join(DATA, "approx_values.csv")).set_index("factor")
e, m = d["danakil"].copy(), d["mars_meridiani"].copy()

# Median slope comes from the notebook (analysis/danakil_mars_slope.ipynb), not the CSV placeholder.
# Run the notebook, then copy its results.csv into data/results.csv.
SLOPE_FILE = os.path.join(DATA, "results.csv")
if not os.path.exists(SLOPE_FILE):
    sys.exit(f"Missing {SLOPE_FILE}: run analysis/danakil_mars_slope.ipynb and copy its results.csv to data/.")
slopes = pd.read_csv(SLOPE_FILE).set_index("site")["median_slope_463m"]
for site in ("Dallol (Danakil)", "Meridiani Planum"):
    if site not in slopes.index or pd.isna(slopes[site]):
        sys.exit(f"{SLOPE_FILE} has no median_slope_463m for '{site}': re-run the notebook.")
e["median_slope"] = float(slopes["Dallol (Danakil)"])
m["median_slope"] = float(slopes["Meridiani Planum"])
print(f"Median slope at ~463 m: Dallol {e['median_slope']:.2f} deg, Meridiani {m['median_slope']:.2f} deg")

SLOPE_SCALE_DEG = 5.0   # slope difference (deg) at which the terrain score falls to 1/e
TEMP_SCALE_C = 50.0     # temperature difference (degC) at which the temperature score falls to 1/e
LOG_DECADES = 3.0       # pressure / dose-rate ratio (orders of magnitude) at which the score reaches 0

def log_score(a, b):
    return float(np.clip(1 - abs(np.log10(a / b)) / LOG_DECADES, 0, 1))

scores = {
    "Mineralogy (sulfates/evaporites)": 0.90,   # judgement placeholder
    "Aqueous acidic-brine history":     0.85,   # judgement placeholder
    "Terrain / slope": float(np.exp(-abs(e["median_slope"] - m["median_slope"]) / SLOPE_SCALE_DEG)),
    "Temperature": float(np.exp(-abs(e["mean_surface_temp"] - m["mean_surface_temp"]) / TEMP_SCALE_C)),
    "Atmosphere": log_score(e["surface_pressure"], m["surface_pressure"]),
    "Gravity": float(min(e["gravity"], m["gravity"]) / max(e["gravity"], m["gravity"])),
    "Radiation": log_score(e["radiation_dose_rate"], m["radiation_dose_rate"]),
}
w_geo = dict(zip(scores, [0.30, 0.25, 0.15, 0.05, 0.05, 0.10, 0.10]))   # science: geochemistry focus
w_ops = dict(zip(scores, [0.05, 0.05, 0.20, 0.25, 0.20, 0.15, 0.10]))   # operations/physical environment focus

for name, w in (("geochem", w_geo), ("ops", w_ops)):
    assert abs(sum(w.values()) - 1) < 1e-9, f"{name} weights must sum to 1"

res = pd.DataFrame({"score": scores, "w_geochem": w_geo, "w_ops": w_ops})
idx_geo = (res.score * res.w_geochem).sum()
idx_ops = (res.score * res.w_ops).sum()
print(res.round(2).to_string())
print(f"\nSimilarity index (geochemistry weighting): {idx_geo:.2f}")
print(f"Similarity index (operations weighting):   {idx_ops:.2f}")
res.round(3).to_csv(os.path.join(DATA, "similarity_scores.csv"))

# Sensitivity: how much do the indices move if the arbitrary scale choices change?
def indices(slope_scale=SLOPE_SCALE_DEG, temp_scale=TEMP_SCALE_C):
    s = dict(scores)
    s["Terrain / slope"] = float(np.exp(-abs(e["median_slope"] - m["median_slope"]) / slope_scale))
    s["Temperature"] = float(np.exp(-abs(e["mean_surface_temp"] - m["mean_surface_temp"]) / temp_scale))
    return sum(s[k] * w_geo[k] for k in s), sum(s[k] * w_ops[k] for k in s)
print("\nSensitivity (geochem / ops index):")
for ss in (1, 2, 5, 10):
    g, o = indices(slope_scale=ss); print(f"  slope scale {ss:>2} deg:   {g:.2f} / {o:.2f}")
for ts in (25, 50, 100):
    g, o = indices(temp_scale=ts); print(f"  temp scale {ts:>3} degC: {g:.2f} / {o:.2f}")

fig, ax = plt.subplots(figsize=(8, 4.5))
cols = ["#2a9d8f" if s >= 0.6 else "#e9c46a" if s >= 0.3 else "#e76f51" for s in res.score]
ax.barh(res.index[::-1], res.score[::-1], color=cols[::-1])
ax.set_xlim(0, 1); ax.set_xlabel("Similarity to Meridiani Planum (0-1, approximate)")
ax.set_title(f"Danakil vs Mars: geochem index {idx_geo:.2f}, operations index {idx_ops:.2f}")
plt.tight_layout(); plt.savefig(os.path.join(FIGS, "similarity_scores.png"), dpi=150)
