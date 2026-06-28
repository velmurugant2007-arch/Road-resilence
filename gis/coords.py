from pyproj import CRS, Transformer
import rasterio
from affine import Affine

class CoordinateManager:
    """
    Handles conversion between pixel space, geographic space (EPSG:4326), 
    and projected metric space (UTM).
    """
    @staticmethod
    def pixel_to_geo(transform: Affine, col: float, row: float) -> tuple[float, float]:
        """Convert pixel coordinates to CRS coordinates based on affine transform."""
        return transform * (col, row)

    @staticmethod
    def geo_to_pixel(transform: Affine, x: float, y: float) -> tuple[float, float]:
        """Convert CRS coordinates to pixel coordinates."""
        # The ~ operator inverts the affine transform
        return ~transform * (x, y)

    @staticmethod
    def reproject(x: float, y: float, src_crs: str | int, dst_crs: str | int) -> tuple[float, float]:
        """
        Reproject geographic coordinates.
        Example: EPSG:4326 (Lat/Lon) to EPSG:32643 (UTM Zone 43N for Bengaluru).
        """
        transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
        return transformer.transform(x, y)
