import rasterio
from rasterio.errors import RasterioIOError
from pathlib import Path
from utils.logger import get_logger

logger = get_logger("gis.loader")

class GeoTIFFLoader:
    """
    Handles the safe ingestion and memory-mapped reading of large satellite GeoTIFFs.
    """
    def __init__(self, file_path: Path | str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            logger.error(f"GeoTIFF file not found: {self.file_path}")
            raise FileNotFoundError(f"GeoTIFF file not found: {self.file_path}")
            
    def get_dataset(self) -> rasterio.DatasetReader:
        """
        Opens the GeoTIFF in read mode. Must be used as a context manager.
        Example:
            with loader.get_dataset() as src:
                print(src.meta)
        """
        try:
            # Using memory mapping for massive files prevents RAM exhaustion
            return rasterio.open(self.file_path, mode='r', sharing=False)
        except RasterioIOError as e:
            logger.critical(f"Failed to open GeoTIFF {self.file_path}. Is it corrupted?")
            raise e
            
    def get_metadata(self) -> dict:
        """
        Extracts crucial GIS metadata including CRS and Affine Transform without reading pixel data.
        """
        with self.get_dataset() as src:
            return {
                "width": src.width,
                "height": src.height,
                "count": src.count, # Number of bands
                "crs": src.crs.to_string() if src.crs else None,
                "transform": src.transform,
                "bounds": src.bounds
            }
