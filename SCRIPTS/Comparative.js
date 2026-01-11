// =============================================================================
// TITLE: Multi-Site Validation & Quantitative Accuracy Assessment (RMSE)
// =============================================================================

// 1. DEFINE MULTIPLE STUDY SITES (Addressing "Single-Site" Critique)
var sites = {
  'Narok_Crops': ee.Geometry.Point([35.95, -1.15]),   // Your original site
  'Kajiado_Shrub': ee.Geometry.Point([36.78, -1.69]), // Semi-arid pastoral
  'Turkana_Bare': ee.Geometry.Point([35.60, 3.10])    // Arid/Desert baseline
};

// Select one site to center the map initially
Map.centerObject(sites['Narok_Crops'], 10);
var startDate = '2023-01-01';
var endDate = '2023-12-31';

// -----------------------------------------------------------------------------
// 2. HELPER FUNCTIONS
// -----------------------------------------------------------------------------

function maskS2clouds(image) {
  var qa = image.select('QA60');
  var mask = qa.bitwiseAnd(1<<10).eq(0).and(qa.bitwiseAnd(1<<11).eq(0));
  return image.updateMask(mask).divide(10000).copyProperties(image, ['system:time_start']);
}

// -----------------------------------------------------------------------------
// 3. THE NOVELTY: ROBUST AUTOMATED EXTRACTION (Applied per site)
// -----------------------------------------------------------------------------
function getAutoEndmembers(img, region) {
  var ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI');
  var bsi = img.expression(
      '((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))', 
      {'B11': img.select('B11'), 'B4': img.select('B4'), 'B8': img.select('B8'), 'B2': img.select('B2')}
  ).rename('BSI'); 
  var brightness = img.reduce(ee.Reducer.sum()).rename('Bright'); 

  // We use 98th percentile (The Plaza et al. approach applied operationally)
  var stats = ndvi.addBands(bsi).addBands(brightness).reduceRegion({
    reducer: ee.Reducer.percentile([2, 98]), 
    geometry: region, 
    scale: 30, 
    maxPixels: 1e9
  });
  
  // Extract pure spectra based on these statistical thresholds
  var vegSpec = img.updateMask(ndvi.gt(ee.Image.constant(stats.get('NDVI_p98'))))
                   .reduceRegion({reducer: ee.Reducer.mean(), geometry: region, scale: 30});
  var soilSpec = img.updateMask(bsi.gt(ee.Image.constant(stats.get('BSI_p98'))))
                    .reduceRegion({reducer: ee.Reducer.mean(), geometry: region, scale: 30});
  var shadowSpec = img.updateMask(brightness.lt(ee.Image.constant(stats.get('Bright_p2'))))
                      .reduceRegion({reducer: ee.Reducer.mean(), geometry: region, scale: 30});
                      
  // Return as a dictionary to use easily later
  var bandOrder = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12'];
  return {
    'soil': bandOrder.map(function(b){ return soilSpec.get(b) }),
    'veg': bandOrder.map(function(b){ return vegSpec.get(b) }),
    'shadow': bandOrder.map(function(b){ return shadowSpec.get(b) })
  };
}






// -----------------------------------------------------------------------------
// 4. MAIN LOOP OVER SITES
// -----------------------------------------------------------------------------

Object.keys(sites).forEach(function(siteName) {
  
  var roi = sites[siteName];
  var bounds = roi.buffer(2000).bounds();
  
  // Load Data
  var dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                  .filterDate(startDate, endDate)
                  .filterBounds(roi)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                  .map(maskS2clouds)
                  .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']);
                  
  // A. Dynamic Endmember Extraction for this specific site
  var referenceImage = dataset.median().clip(bounds);
  var em = getAutoEndmembers(referenceImage, bounds);
  var endmemberList = [em.soil, em.veg, em.shadow];
  
  print(siteName + ' Endmembers:', endmemberList);

  // B. Unmixing + RMSE CALCULATION (Addressing "Accuracy" Critique)
  var processed = dataset.map(function(image) {
    
    // 1. Unmix (endmemberList order: Soil, Veg, Shadow)
    // This produces bands in order: [0]=Soil, [1]=Veg, [2]=Shadow
    var unmixed = image.unmix(endmemberList).max(0);
    var total = unmixed.reduce(ee.Reducer.sum());
    var normalized = unmixed.divide(total);
    
    // 2. REORDER bands to alphabetical: Shadow, Soil, Veg
    // Select band 2 (Shadow), band 0 (Soil), band 1 (Veg)
    var fractions = ee.Image.cat([
      normalized.select([2]),  // Shadow data
      normalized.select([0]),  // Soil data
      normalized.select([1])   // Veg data
    ]).rename(['Shadow', 'Soil', 'Veg']);
    
    // 3. Calculate RMSE (Reconstruction Error)
    // Now bands are correctly ordered: Shadow=Shadow, Soil=Soil, Veg=Veg
    
    // Create constant images for endmembers
    var soilImg = ee.Image.constant(em.soil);
    var vegImg = ee.Image.constant(em.veg);
    var shadowImg = ee.Image.constant(em.shadow);
    
    // Reconstruct bands (Weighted sum)
    var modeled = soilImg.multiply(fractions.select('Soil'))
        .add(vegImg.multiply(fractions.select('Veg')))
        .add(shadowImg.multiply(fractions.select('Shadow')));
    
    // Compare Modeled vs Observed (Original Image)
    var diff = image.subtract(modeled).pow(2); // Square the difference
    var rmse = diff.reduce(ee.Reducer.mean()).sqrt().rename('RMSE'); // Mean of squares, then Sqrt
    
    return fractions.addBands(rmse).copyProperties(image, ['system:time_start']);
  });
  
  // ---------------------------------------------------------------------------
  // CORRECTED CHART: NOW INCLUDES SHADOW
  // ---------------------------------------------------------------------------
  
  print(ui.Chart.image.series({
    imageCollection: processed.select(['Shadow', 'Soil', 'Veg']),
    region: bounds,
    reducer: ee.Reducer.mean(),
    scale: 30
  }).setOptions({
    title: siteName + ': Soil, Veg, and Shadow Dynamics',
    vAxis: {title: 'Fractional Cover (0-1)'},
    lineWidth: 2,
    series: {
      0: {color: 'blue', labelInLegend: 'Shadow/Moisture'},
      1: {color: 'red', labelInLegend: 'Soil'},
      2: {color: 'green', labelInLegend: 'Vegetation'}
    }
  }));
  
  
  
  
  
  
  
  // ---------------------------------------------------------------------------
  // 5. OUTPUTS PER SITE
  // ---------------------------------------------------------------------------
  
  // Chart: Soil Trends
  print(ui.Chart.image.series({
    imageCollection: processed.select(['Soil', 'Veg']),
    region: bounds,
    reducer: ee.Reducer.mean(),
    scale: 30
  }).setOptions({
    title: siteName + ': Soil vs Veg Dynamics',
    vAxis: {title: 'Fraction'},
    series: {0: {color: 'red', labelInLegend: 'Soil'}, 1: {color: 'green', labelInLegend: 'Vegetation'}}
  }));
  
  // Chart: RMSE (The Accuracy Metric)
  // Low RMSE (<0.05) means the model is physically valid. High RMSE means error.
  print(ui.Chart.image.series({
    imageCollection: processed.select('RMSE'),
    region: bounds,
    reducer: ee.Reducer.mean(),
    scale: 30
  }).setOptions({
    title: siteName + ': Model Accuracy (RMSE)',
    vAxis: {title: 'RMSE (Lower is Better)'},
    colors: ['black']
  }));
  
  // Add Layer to Map (Visual Check)
  Map.addLayer(processed.select('Soil').mean().clip(bounds), {min:0, max:1, palette:['white', 'red']}, siteName + ' Mean Soil');
  
  // ---------------------------------------------------------------------------
  // 6. NAROK-SPECIFIC VALIDATION & EXPORT
  // ---------------------------------------------------------------------------
  
  if (siteName === 'Narok_Crops') {
    
    // Find the single clearest image in the Harvest Season (Aug-Sept)
    var validationImage = dataset.filterDate('2023-08-01', '2023-09-30')
                                 .sort('CLOUDY_PIXEL_PERCENTAGE')
                                 .first();
    
    if (validationImage) {
      print('Narok Validation Image Found for Date:', validationImage.date());
      var valClipped = validationImage.clip(bounds);
      
      // Unmix this specific image
      var valUnmixed = valClipped.unmix(endmemberList);
      var valNonNeg = valUnmixed.max(0);
      var valSum = valNonNeg.reduce(ee.Reducer.sum());
      var valNormalized = valNonNeg.divide(valSum);
      
      // Reorder to alphabetical: Shadow, Soil, Veg
      var valFractions = ee.Image.cat([
        valNormalized.select([2]),  // Shadow
        valNormalized.select([0]),  // Soil
        valNormalized.select([1])   // Veg
      ]).rename(['Shadow', 'Soil', 'Veg']);
      
      var valSoil = valFractions.select('Soil').rename('Soil_Fraction');
      
      // Visualization Parameters
      var visRGB = {min: 0, max: 0.3, bands: ['B4', 'B3', 'B2']};
      var visSoil = {min: 0, max: 1, palette: ['white', 'orange', 'red']};
      
      // Add Layers to Map for Visual Validation
      Map.addLayer(valClipped, visRGB, 'Narok (A) True Color Reference');
      Map.addLayer(valSoil, visSoil, 'Narok (B) Soil Fraction Model');
      
      // Export Tasks (Go to "Tasks" tab to run these)
      
      // Export 1: Time Series CSV Data
      var statsTable = processed.map(function(img) {
        var stats = img.select(['Shadow', 'Soil', 'Veg']).reduceRegion({
          reducer: ee.Reducer.mean(), 
          geometry: roi, 
          scale: 30
        });
        return ee.Feature(null, stats).set('date', img.date().format('YYYY-MM-dd'));
      });
      
      Export.table.toDrive({
        collection: statsTable,
        description: 'Narok_TimeSeries_Data',
        fileFormat: 'CSV'
      });
      
      // Export 2: Validation Soil Fraction Map (for QGIS Figure)
      Export.image.toDrive({
        image: valSoil,
        description: 'Narok_Soil_Fraction_Map',
        scale: 10,
        region: bounds,
        fileFormat: 'GeoTIFF'
      });
      
      // Export 3: True Color Reference (for QGIS Figure)
      Export.image.toDrive({
        image: valClipped.select(['B4', 'B3', 'B2']),
        description: 'Narok_TrueColor_Ref',
        scale: 10,
        region: bounds,
        fileFormat: 'GeoTIFF'
      });
      
      print('✓ Narok export tasks created. Check the Tasks tab to run them.');
      
    } else {
      print('⚠ WARNING: No clear validation image found for Narok in Aug-Sept period.');
    }
  }
});