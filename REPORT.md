# The Danakil Depression, Ethiopia: An Underused Analog for Acidic, Salt-Rich Mars

## 1. Objective
Most Mars analog research focuses on the Atacama, Antarctica, Iceland, and Hawaii. This project proposes the Danakil Depression (Afar, Ethiopia), including the Dallol hydrothermal area, as an analog for Martian environments where acidic, salty water once existed, such as Meridiani Planum, where Opportunity found jarosite and sulfate-rich rocks.

## 2. Why This Site
- About 100 m or more below sea level, in a rift basin with salt flats, evaporites, and active hydrothermal springs.
- Dallol's pools are extremely acidic and hypersaline, near the limits of known life, useful for learning to distinguish lifeless from life-bearing environments.
- One of the hottest inhabited regions on Earth, which stresses equipment and human operations.

## 3. Data and Method
| Dimension | Earth data | Mars data |
|---|---|---|
| Topography (**used**) | Copernicus GLO-30 DEM | MOLA 463 m DEM |
| Surface temperature (planned) | MODIS LST | THEMIS |
| Mineralogy (planned) | ASTER spectral indices | CRISM / OMEGA |
| Imagery (planned) | Landsat, Sentinel-2 | HiRISE, CTX |

Slope is computed in `analysis/danakil_mars_slope.ipynb` over a 20 km box at each site. Earth DEMs are block-averaged to about 463 m pixels so they match MOLA, because median slope depends strongly on pixel size. Mars distances use the MOLA radius (3396.19 km).

Each factor is scored 0 to 1 (`analysis/similarity.py`) and combined with two weight sets: geochemistry-focused and operations-focused.

| Site | Median slope at ~463 m (deg) |
|---|---|
| Dallol (Danakil) | 0.03 |
| Atacama | 2.92 |
| Haughton Crater | 2.11 |
| Death Valley | 3.90 |
| Meridiani Planum (Mars) | 0.26 |

## 4. Results (approximate)
| Factor | Score |
|---|---|
| Mineralogy (sulfates/evaporites) | 0.90 (judgement) |
| Aqueous acidic-brine history | 0.85 (judgement) |
| Terrain / slope | 0.96 (MOLA / Copernicus DEM, median slope at ~463 m) |
| Temperature | 0.15 |
| Atmosphere | 0.26 |
| Gravity | 0.38 |
| Radiation | 0.34 |

Geochemistry-weighted index: **0.72**. Operations-weighted index: **0.46**. See `figures/similarity_scores.png` and `figures/median_slope_463m.png`.

Sensitivity: changing the slope scale (1 to 10 deg) and temperature scale (25 to 100 degC) moves the geochemistry index between 0.69 and 0.73 and the operations index between 0.43 and 0.52, so the conclusions do not depend on those choices.

## 5. Where the Analogy Breaks Down
Danakil is hot, wet at the springs, under about 1 bar of air with low radiation and 1 g. Mars is cold, dry, about 6 mbar, radiation-exposed, and 0.38 g. Danakil analogs chemistry, mineralogy, and water-rock processes, not climate. Pair it with cold-desert sites such as Antarctica's Dry Valleys.

## 6. Value for Exploration
- Instrument testing (Raman, XRD, infrared) on real sulfate and evaporite deposits.
- Biosignature protocol development in extreme brines.
- Helps rank Mars landing sites by understanding evaporite formation and preservation.
- Tests field logistics and robot durability in heat, salt, and remoteness.

## 7. Conclusion
Danakil is a strong geochemical analog and a poor climatic one. A transparent, weighted index makes both explicit, and the weighting shows that "how good an analog" depends on the exploration goal.

## 8. Limitations of this study
Slope is computed from DEMs; temperature, pressure, gravity and radiation are approximate literature values; mineralogy and aqueous-history scores are judgement-based. Next steps are MODIS LST vs THEMIS temperatures and ASTER vs CRISM sulfate maps.

## References (complete before submitting)
- Copernicus DEM GLO-30: produced using Copernicus data and information funded by the European Union (accessed via AWS Open Data)
- MOLA MGS global DEM 463 m (Smith et al., 2003), via USGS Astrogeology
- NASA Earthdata (MODIS, ASTER); USGS Landsat
- NASA Planetary Data System (MOLA, CRISM, HiRISE, THEMIS)
- Papers on Dallol geochemistry and Meridiani Planum sulfates (Opportunity results)
