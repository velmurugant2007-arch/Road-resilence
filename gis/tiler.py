import rasterio
from rasterio.windows import Window
import numpy as np
from typing import Iterator, Tuple
from utils.logger import get_logger

logger = get_logger("gis.tiler")

class GeoTiler:
    """
    Slices massive satellite imagery into trainable/inferable windows (e.g., 512x512).
    """
    def __init__(self, tile_size: int = 512, overlap: int = 0):
        self.tile_size = tile_size
        self.overlap = overlap
        self.stride = tile_size - overlap

    def generate_windows(self, width: int, height: int) -> Iterator[Tuple[int, int, Window]]:
        """
        Yields rasterio Windows to read the image in chunks.
        Returns: (col_offset, row_offset, Window)
        """
        for col_off in range(0, width, self.stride):
            for row_off in range(0, height, self.stride):
                # Ensure we don't read past the edges
                w = min(self.tile_size, width - col_off)
                h = min(self.tile_size, height - row_off)
                
                window = Window(col_off, row_off, w, h)
                yield col_off, row_off, window

    def extract_tile(self, src: rasterio.DatasetReader, window: Window) -> np.ndarray:
        """
        Reads only the pixels within the specified Window from the disk into RAM.
        Expected output shape: (Channels, Height, Width)
        """
        # Read the windowed data
        tile_data = src.read(window=window)
        
        # If the tile at the edge of the image is smaller than tile_size, pad it with zeros
        _, h, w = tile_data.shape
        if h < self.tile_size or w < self.tile_size:
            pad_h = self.tile_size - h
            pad_w = self.tile_size - w
            # Pad with 0s at the end of H and W dimensions
            tile_data = np.pad(tile_data, ((0, 0), (0, pad_h), (0, pad_w)), mode='constant', constant_values=0)
            
        return tile_data
