import pytest
import numpy as np
import rasterio
from rasterio.transform import from_origin
import os
import time
from pathlib import Path

from gis.loader import GeoTIFFLoader
from gis.tiler import GeoTiler
from gis.transform import GISTransformer
from gis.coords import CoordinateManager

TEST_TIFF_PATH = Path("temp_test.tif")

@pytest.fixture(scope="module", autouse=True)
def setup_mock_geotiff():
    # Create a 3-channel 1024x1024 mock image
    data = np.random.randint(0, 255, (3, 1024, 1024), dtype=np.uint8)
    # Origin at 77.5 Lon, 12.9 Lat (Bengaluru roughly), pixel size 0.0001 degrees
    transform = from_origin(77.5, 12.9, 0.0001, 0.0001)
    
    with rasterio.open(
        TEST_TIFF_PATH, 'w',
        driver='GTiff', width=1024, height=1024, count=3,
        dtype=str(data.dtype), crs='EPSG:4326', transform=transform
    ) as dataset:
        dataset.write(data)
        
    yield
    
    # Cleanup
    if TEST_TIFF_PATH.exists():
        os.remove(TEST_TIFF_PATH)

def test_loader_validation():
    loader = GeoTIFFLoader(TEST_TIFF_PATH)
    meta = loader.get_metadata()
    assert meta["width"] == 1024
    assert meta["height"] == 1024
    assert meta["count"] == 3
    assert "4326" in meta["crs"]
    
def test_tiler_validation():
    loader = GeoTIFFLoader(TEST_TIFF_PATH)
    tiler = GeoTiler(tile_size=512, overlap=0)
    
    tiles = []
    with loader.get_dataset() as src:
        for col_off, row_off, window in tiler.generate_windows(src.width, src.height):
            tile = tiler.extract_tile(src, window)
            tiles.append(tile)
            assert tile.shape == (3, 512, 512)
            
    # 1024x1024 with 512 tile size -> exactly 4 tiles
    assert len(tiles) == 4

def test_coordinate_validation():
    loader = GeoTIFFLoader(TEST_TIFF_PATH)
    meta = loader.get_metadata()
    transform = meta["transform"]
    
    # Pixel to Geo
    lon, lat = CoordinateManager.pixel_to_geo(transform, 0, 0)
    assert lon == 77.5
    assert lat == 12.9
    
    # Geo to Pixel
    col, row = CoordinateManager.geo_to_pixel(transform, lon, lat)
    assert col == 0.0
    assert row == 0.0
    
    # Reprojection EPSG:4326 -> EPSG:32643 (UTM 43N for Bengaluru) -> EPSG:4326
    x, y = CoordinateManager.reproject(lon, lat, "EPSG:4326", "EPSG:32643")
    assert x != lon  # Reprojected to meters
    lon2, lat2 = CoordinateManager.reproject(x, y, "EPSG:32643", "EPSG:4326")
    assert pytest.approx(lon) == lon2
    assert pytest.approx(lat) == lat2

def test_normalization_validation():
    # Synthetic tile data [C, H, W] in 0-255 range
    tile_data = np.full((3, 512, 512), 128, dtype=np.uint8)
    transformer = GISTransformer()
    
    tensor = transformer.to_model_tensor(tile_data)
    
    # Expected ImageNet normalized values for 128/255.0 (~0.5019)
    # Channel 0: (0.5019 - 0.485) / 0.229 = 0.074
    assert tensor.shape == (3, 512, 512)
    assert tensor.is_floating_point()
    assert -3.0 < tensor.min() < 3.0  # Normalized bounds check
