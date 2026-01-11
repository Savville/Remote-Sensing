This is a comprehensive **Project Guideline** designed to structure your work as a formal technical paper or advanced research project.

This outline elevates the work from a "standard remote sensing task" to a **research-grade investigation** suitable for submission to IEEE GRSS or similar venues.

### ---

**Project Title**

**"Spatiotemporal Dynamics of Land Degradation: A Novel Automated Temporal Spectral Unmixing Approach in the Kenyan Rift Valley"**

### ---

**1\. Introduction & Theoretical Background**

#### **1.1 The Problem: The "Mixed Pixel" Challenge**

Standard monitoring uses indices like **NDVI** (Normalized Difference Vegetation Index).

* **Limitation:** In semi-arid regions (like Narok or Kajiado), vegetation is sparse. A single $10m \\times 10m$ Sentinel-2 pixel often contains a mix of **50% bare soil, 30% acacia shrub, and 20% dry grass**.  
* **Failure Mode:** NDVI averages this into a single number. A drop in NDVI could mean "dead plants" *or* just "dryer soil background." It cannot distinguish between the two.

#### **1.2 The Solution: Linear Spectral Mixture Analysis (LSMA)**

Instead of averaging the pixel, we "unmix" it. We assume the reflectance ($R$) of a pixel is a linear sum of its components (Endmembers), weighted by their area fraction ($f$).

$$R\_{pixel} \= (f\_{veg} \\times R\_{veg}) \+ (f\_{soil} \\times R\_{soil}) \+ (f\_{shadow} \\times R\_{shadow}) \+ \\epsilon$$

* **$R$**: Reflectance (Satellite Data)  
* **$f$**: Fraction (What we want to calculate: e.g., 0.60 Vegetation)  
* **$\\epsilon$**: Residual Error

#### **1.3 The Novelty (Your "Sales Pitch")**

Standard unmixing papers use **static endmembers** (e.g., one fixed "Soil" spectrum from a library).

* **Your Innovation:** **Automated Temporal Endmember Extraction (ATEE).**  
* **Why it matters:** Soil in Kenya changes color when wet (darker) vs. dry (brighter). Using a static "Red Soil" signature will fail during the rainy season. Your code calculates *dynamic* endmembers for every image automatically, adapting to seasonality.

### ---

**2\. Methodology & Workflow**

This is the step-by-step technical execution plan.

#### **Phase 1: Data Pre-processing (The Foundation)**

1. **Input:** Sentinel-2 Level-2A (Surface Reflectance).  
2. **Filtering:** Filter by Cloud Cover (\<20%) and ROI (Narok/Rift Valley).  
3. **Masking:** Apply strict Cloud & Shadow masking (using QA60 band).  
   * *Critical Detail:* Clouds are often confused for bright soil. Shadow is confused for water. Strict masking is mandatory.

#### **Phase 2: Automated Endmember Extraction (The Core Algorithm)**

Instead of manual selection, you use statistical extremity:

1. **Vegetation Endmember:** The pixel with the 99th percentile **NDVI** in the scene.  
2. **Soil Endmember:** The pixel with the 99th percentile **BSI** (Bare Soil Index) or highest brightness.  
3. **Shadow Endmember:** The darkest 1% of pixels (lowest sum of bands).  
4. **Novelty Step:** This extraction happens *dynamically*. If the soil is wet in April, the algorithm finds the "purest wet soil" and uses that signature.

#### **Phase 3: Constrained Spectral Unmixing**

Run the unmixing using the extracted signatures.

1. **Unconstrained Solve:** GEE solves the linear equations.  
2. **Constraint Application:**  
   * **Non-Negativity:** $f \\ge 0$ (Negative fractions are physically impossible).  
   * **Sum-to-One:** $\\sum f \= 1$ (The fractions must add up to 100% of the pixel).

#### **Phase 4: Time-Series Analysis**

1. **Transformation:** Convert the stack of images into a **Fractional Time Series**.  
2. **Metric Calculation:**  
   * **Degradation Proxy:** The rate of increase in the **Soil Fraction ($f\_{soil}$)** over time.  
   * **Resilience Proxy:** How fast $f\_{veg}$ recovers after the dry season.

### ---

**3\. Expected Results & Interpretations**

When writing your discussion, you will look for these three signals:

| Signal Pattern | Physical Interpretation |
| :---- | :---- |
| **Rising Soil ($f\_{soil}$) \+ Falling Veg ($f\_{veg}$)** | **Land Degradation / Erosion.** The vegetation is thinning, exposing more ground. |
| **Spike in Shadow ($f\_{shadow}$)** | **Moisture Event.** In unmixing, wet soil looks like "Shadow." A spike here usually correlates with rainfall data (CHIRPS). |
| **Stable Veg ($f\_{veg}$) but Decreasing NDVI** | **Browning.** The leaves are still there (high fraction), but they are turning brown (lower NDVI). This distinguishes "Drought Stress" from "Deforestation." |

### ---

**4\. Validation Strategy (How to prove it works)**

To publish, you must validate your model. Since you cannot go back in time to sample soil, use **"Cross-Sensor Validation."**

1. **High-Res Truth:** Find a Google Earth Image (high res) of your area from a specific date (e.g., Jan 2024).  
2. **Visual Classification:** Manually estimate the vegetation cover in a small plot (e.g., "This plot looks like 50% trees").  
3. **Model Comparison:** Check if your GEE script calculated \~0.50 Veg Fraction for that same date.  
4. **Scatter Plot:** Plot *Predicted Fraction* (Y-axis) vs. *Observed Fraction* (X-axis). A high $R^2$ (correlation) proves accuracy.

### ---

**5\. Summary of Novelty for the Paper**

When you write the **Abstract**, use this exact framing:

*"While spectral unmixing is an established technique, traditional methods rely on static endmembers that fail to account for the high seasonal spectral variability of semi-arid Kenyan soils. This study introduces an **Automated Temporal Endmember Extraction (ATEE)** workflow in Google Earth Engine. By dynamically deriving pure spectral signatures for every time-step, we significantly reduce the 'Soil-Shadow' confusion common in tropical remote sensing, providing a more robust early-warning system for soil erosion than conventional vegetation indices."*