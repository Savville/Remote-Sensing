# Spectral Unmixing Chart Generation

## Overview
This directory contains the automated chart generation script for the IEEE GRSS paper **"Automated Temporal Spectral Unmixing for Land Degradation Monitoring in Semi-Arid Kenya"**.

## Files

### Main Script
- **`GenerateCharts.py`** - Main Python script that generates all publication-quality figures from CSV data

### Data Sources (DATA/ directory)
- `Narok_Crops Soil Veg and Shadow Dynamics.csv` - Fractional cover time series for Narok agricultural site
- `Kajiado_Shrub Soil Veg and Shadow Dynamics.csv` - Fractional cover time series for Kajiado shrubland site  
- `Turkana_Bare Soil Veg and Shadow Dynamics.csv` - Fractional cover time series for Turkana arid site
- `Narok_Crops Model Accuracy_RMSE.csv` - RMSE accuracy metrics for Narok
- `Kajiado_Shrub Model Accuracy RMSE.csv` - RMSE accuracy metrics for Kajiado
- `Turkana_Bare Model Accuracy RMSE.csv` - RMSE accuracy metrics for Turkana

## Generated Figures (IMAGES/ directory)

### Main Publication Figures

#### **Figure 3: Narok Temporal Dynamics**
- `Figure3_Narok_Temporal_Dynamics.png` (300 DPI)
- `Figure3_Narok_Temporal_Dynamics_HighRes.tiff` (600 DPI for publication)

**Description:** Four-panel time series showing:
- (A) Soil fraction temporal evolution
- (B) Vegetation fraction temporal evolution  
- (C) Shadow fraction temporal evolution
- (D) RMSE reconstruction accuracy

**Key features:**
- Vertical dashed lines marking phenological events (Long Rains onset, Harvest, El Niño onset)
- Shaded areas showing fractional trends
- RMSE threshold line at 0.10 (operational acceptance criterion)

---

#### **Figure 4: Multi-Site Comparison**
- `Figure4_MultiSite_Comparison.png` (300 DPI)
- `Figure4_MultiSite_Comparison_HighRes.tiff` (600 DPI for publication)

**Description:** Six-panel comparative analysis:
- (A) Narok Soil + Vegetation dynamics
- (B) Narok RMSE accuracy
- (C) Kajiado Soil + Vegetation dynamics
- (D) Kajiado RMSE accuracy
- (E) Turkana Soil + Vegetation dynamics
- (F) Turkana RMSE accuracy

**Key features:**
- Consistent axis scales for direct cross-site comparison
- Embedded statistics boxes showing mean, median, and % good fit
- Color-coded by site for easy identification

---

### Supplementary Figures

#### **Individual Site Complete Analysis**
- `Narok_Complete_Analysis.png`
- `Kajiado_Complete_Analysis.png`
- `Turkana_Complete_Analysis.png`

**Description:** Detailed two-panel charts for each site:
- Top: Stacked area chart showing all three fractions (Soil, Vegetation, Shadow) cumulative to 1.0
- Bottom: RMSE time series with threshold line

---

#### **Cross-Site RMSE Comparison**
- `RMSE_MultiSite_BoxPlot.png`

**Description:** Box-and-whisker plot comparing RMSE distributions across three sites
- Shows median, quartiles, outliers, and mean (red diamond)
- Color-coded: Green (Narok), Gold (Kajiado), Coral (Turkana)
- Statistical annotations (mean, median, % good fit)
- Red dashed line at 0.10 operational threshold

---

#### **Summary Statistics Table**
- `Table1_RMSE_Summary.png`

**Description:** Publication-ready table showing:
- Site-specific RMSE statistics (mean, median, std dev, min, max)
- Number of observations per site
- Percentage of observations achieving "good fit" (RMSE ≤ 0.10)
- Overall aggregated statistics

---

## Running the Script

### Requirements
```bash
pip install pandas matplotlib numpy
```

### Execution
```bash
cd "c:\Users\User\Documents\RESEARCH\IGARSS\Spectral unmixing"
python GenerateCharts.py
```

### Expected Output
```
============================================================
Spectral Unmixing Figure Generation Script
============================================================

Loading data files...
✓ Loaded 6 datasets

Generating figures...

✓ Saved: IMAGES\Figure3_Narok_Temporal_Dynamics.png
✓ Saved: IMAGES\Figure3_Narok_Temporal_Dynamics_HighRes.tiff
✓ Saved: IMAGES\Figure4_MultiSite_Comparison.png
✓ Saved: IMAGES\Figure4_MultiSite_Comparison_HighRes.tiff
✓ Saved: IMAGES\Narok_Complete_Analysis.png
✓ Saved: IMAGES\Kajiado_Complete_Analysis.png
✓ Saved: IMAGES\Turkana_Complete_Analysis.png
✓ Saved: IMAGES\RMSE_MultiSite_BoxPlot.png
✓ Saved: IMAGES\Table1_RMSE_Summary.png

============================================================
✓ All figures generated successfully!
✓ Output directory: IMAGES
============================================================
```

---

## Key Findings Visualized

### Narok Agricultural Zone (Figure 3)
- **Drought-to-El Niño transition captured:** Vegetation fraction increased from 5% (Feb) to 60% (Dec)
- **12-fold vegetation increase** during 2023 El Niño event
- **RMSE remained stable** (mean 0.055) across full seasonal cycle
- Shadow component correctly distinguished from wet soil

### Multi-Site Robustness (Figure 4)
- **Narok (cropland):** Lowest RMSE (0.055), highest spectral contrast
- **Kajiado (shrubland):** Highest variability (SD 0.044), woody vegetation complexity
- **Turkana (arid):** Consistent accuracy (median 0.045) despite extreme aridity
- **Overall performance:** 90% of observations achieved RMSE < 0.10

### Cross-Site RMSE Analysis
- **Geographic transferability demonstrated** across three distinct biomes
- **Operational threshold met** in >85% of observations for all sites
- **Temporal stability maintained** across wet and dry seasons

---

## Publication Usage

### For IEEE GRSS Manuscript
1. Use **high-resolution TIFF versions** for final submission:
   - `Figure3_Narok_Temporal_Dynamics_HighRes.tiff`
   - `Figure4_MultiSite_Comparison_HighRes.tiff`

2. Use **PNG versions** for manuscript drafts and reviews

### Figure Captions (Suggested)

**Figure 3:**
> Temporal dynamics of endmember fractions and reconstruction accuracy for Narok agricultural zone during 2023. Panels show (A) soil fraction, (B) vegetation fraction, (C) shadow fraction, and (D) RMSE accuracy. Vertical dashed lines indicate key phenological events: Long Rains onset (March 4, blue), harvest period (August 1, orange), and El Niño onset (November 29, green). The red dotted line in panel D marks the 0.10 RMSE threshold for operational acceptance. Note the 12-fold vegetation increase from February drought (5%) to December El Niño (60%), while RMSE remained below threshold (mean = 0.055).

**Figure 4:**
> Multi-site comparative analysis across three biomes in Kenya. Left column (A, C, E) shows soil (brown) and vegetation (green) fractional cover time series. Right column (B, D, F) displays corresponding RMSE accuracy metrics. Sites span agricultural intensification (Narok, top), pastoral rangeland (Kajiado, middle), and extreme aridity (Turkana, bottom). Red dotted lines mark the 0.10 RMSE operational threshold. Inset statistics show mean/median RMSE and percentage of observations achieving good fit. Note consistent algorithmic performance (>85% good fit) across all three distinct environments.

---

## Technical Notes

### Color Schemes
- **Soil:** Brown/tan palette (`#D2691E`, `#8B4513`, `#CD853F`, `#DEB887`)
- **Vegetation:** Green palette (`#228B22`, `#2E8B57`, `#3CB371`, `#90EE90`)
- **Shadow:** Blue palette (`#4169E1`)
- **RMSE:** Black with gray shading

### Figure Dimensions
- Figure 3: 12" × 10" (4 vertical panels)
- Figure 4: 16" × 12" (3×2 grid)
- Individual site charts: 14" × 8"
- Box plot: 10" × 6"
- Summary table: 12" × 4"

### Resolution Standards
- Draft/review: 300 DPI PNG
- Publication submission: 600 DPI TIFF
- Screen presentation: 300 DPI PNG

---

## Reproducibility

All figures are **fully reproducible** from the source CSV data. The script:
- Requires no manual intervention
- Uses consistent styling across all figures
- Automatically calculates statistics
- Handles date parsing and formatting
- Enforces IEEE publication standards

To regenerate all figures after data updates:
```bash
python GenerateCharts.py
```

---

## Contact
For questions about chart generation or data processing, refer to the main manuscript methodology (Section III) or contact the corresponding author.

**Last Updated:** January 2026  
**Script Version:** 1.0  
**Python Version:** 3.12+  
**Dependencies:** pandas 2.x, matplotlib 3.x, numpy 1.x
