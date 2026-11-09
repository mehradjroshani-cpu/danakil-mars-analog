# Danakil Depression as a Mars Analog

Project for the NASA-style challenge *"Earth as a laboratory for the Moon and Mars"*.
Proposes the Danakil Depression (Dallol, Ethiopia) as an under-used analog for **acidic, salt-rich Mars**
(Meridiani Planum), with a simple, transparent similarity index.

## Contents
- `REPORT.md` – full written report
- `analysis/similarity.py` – computes the similarity index and figure
- `analysis/danakil_mars_slope.ipynb` – computes matched-resolution (~463 m) median slope for Dallol, three other Earth analogs and Meridiani Planum
- `data/approx_values.csv` – input values (**approximate**, see notes)
- `data/results.csv` – slope results from the notebook
- `data/similarity_scores.csv` – output scores
- `figures/similarity_scores.png` – result chart
- `figures/median_slope_463m.png` – slope comparison chart

## Run
The notebook is saved with its outputs, so you can read the results on GitHub without running anything.

1. Run the notebook `analysis/danakil_mars_slope.ipynb` (needs internet for the Copernicus DEM tiles):
   - **Colab:** Runtime > Run all. It downloads the ~2 GB MOLA GeoTIFF from USGS automatically. Download the `results.csv` it creates.
   - **Locally:** download [`Mars_MGS_MOLA_DEM_mosaic_global_463m.tif`](https://planetarymaps.usgs.gov/mosaic/Mars_MGS_MOLA_DEM_mosaic_global_463m.tif) (about 2 GB), set `MOLA_PATH` to its path, and run all cells.
2. Put `results.csv` in `data/results.csv`.
3. Then:
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python analysis/similarity.py
```

## Important limitations
- Slope is computed from DEMs (Copernicus GLO-30 and MOLA 463 m). The other physical inputs are approximate literature-style values.
- Mineralogy and aqueous-history scores are expert-judgement placeholders.
- Next step: temperature from MODIS LST vs THEMIS and sulfate maps from ASTER vs CRISM, then replace the CSV values.
- Verify all numbers and add full citations before submitting.

## Results (approximate)
- Geochemistry-weighted similarity: **0.72**
- Operations-weighted similarity: **0.46**
Danakil is a strong chemistry/mineralogy analog and a weak climate/physical analog.

## Use of AI tools
Claude (Anthropic) was used as a coding assistant to review the analysis code, fix bugs in the slope calculation (matched 463 m resampling, Mars radius, projection scale), add input checks and a sensitivity analysis to `similarity.py`, run the pipeline, and correct factual details in this README and the report. Site choice, the scoring approach, judgement scores and interpretation are the team's own.
