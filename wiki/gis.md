# Geographic Information Systems (GIS)

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> This page documents GIS concepts, coordinate systems, projection handling, and spatial analysis techniques relevant to the project.

---

## Problem Context

The GIS module bridges satellite imagery (raster, georeferenced) and road network analysis (vector, topological). It handles coordinate transformations, spatial indexing, and geographic data management.

---

## Key Concepts

### Coordinate Reference Systems (CRS)
- **WGS84 (EPSG:4326)** — Global geographic coordinates (lat/lon). Standard for GPS and satellite data.
- **UTM Zones** — Projected coordinates (meters). Suitable for distance calculations.
- **Indian CRS** — May be required for ISRO-specific datasets.

### Raster vs. Vector Data
- **Raster**: Satellite imagery (pixels with spectral values, georeferenced)
- **Vector**: Road networks (lines, polygons with attributes, georeferenced)

### Spatial Resolution
- The pixel size in ground units (e.g., 0.5m, 1m, 10m per pixel)
- Determines minimum detectable road width
- Critical for algorithm parameterization

---

## GIS Processing Pipeline

```
Raw Satellite Image (GeoTIFF)
        ↓
   CRS Verification / Transformation
        ↓
   Tiling (large images → manageable tiles)
        ↓
   Normalization (radiometric correction)
        ↓
   AI Inference (per tile)
        ↓
   Tile Reassembly (stitch predictions)
        ↓
   Vectorization (raster mask → vector road lines)
        ↓
   Graph Construction (vector → topology)
        ↓
   Georeferenced Output (Shapefile / GeoJSON / GeoPackage)
```

---

## Libraries to Evaluate

| Library | Purpose | Notes |
|---|---|---|
| Rasterio | Raster I/O, CRS handling | Core raster library |
| Fiona / GeoPandas | Vector data handling | Spatial DataFrames |
| Shapely | Geometry operations | 2D computational geometry |
| PyProj | CRS transformations | Projection engine |
| GDAL/OGR | Comprehensive GIS toolkit | Low-level, powerful |
| Folium / Leaflet | Interactive maps | Dashboard visualization |

---

## Data Formats

| Format | Type | Use Case |
|---|---|---|
| GeoTIFF | Raster | Satellite imagery input |
| Shapefile | Vector | Road network output |
| GeoJSON | Vector | Web-compatible output |
| GeoPackage | Vector/Raster | Modern, SQLite-based |
| COG (Cloud Optimized GeoTIFF) | Raster | Efficient streaming |

---

*This page is updated after every GIS-related research finding and decision.*
