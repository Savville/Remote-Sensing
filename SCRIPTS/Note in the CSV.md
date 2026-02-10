# CSV Manual Column Switching

## Issue with Original Output
The CSV output from the GEE script has columns in the wrong order:
- "Shadow" column contains → Soil data
- "Soil" column contains → Vegetation data  
- "Veg" column contains → Shadow data

## Solution: Manual CSV Column Reordering
Instead of modifying the GEE script, we are manually switching the column headers in the CSV file.

### Original CSV Header:
```
system:time_start,Shadow,Soil,Veg
```

### Corrected CSV Header:
```
system:time_start,Soil,Veg,Shadow
```

The data values remain in the same positions, but the column names are reordered to correctly label what each column represents.
