"""
Fractal mathematics engine for FOLD
"""

import numpy as np
from typing import Tuple, Generator
import zlib

class FractalEncoder:
    """Fractal-based data encoding engine"""
    
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.pixels_per_frame = width * height
        
    def encode_data_to_pixels(self, data: bytes) -> Generator[np.ndarray, None, None]:
        """
        Encode binary data into fractal pixel patterns
        
        Args:
            data: Binary data to encode
            
        Yields:
            numpy arrays representing RGB frames
        """
        # Convert data to bit string with header
        bit_string = self._prepare_bit_string(data)
        
        # Process in chunks that fit in frame
        bits_per_frame = self.pixels_per_frame * 3  # RGB channels
        
        for i in range(0, len(bit_string), bits_per_frame):
            chunk = bit_string[i:i + bits_per_frame]
            frame = self._bits_to_fractal_frame(chunk)
            yield frame
    
    def decode_pixels_to_data(self, frames: list) -> bytes:
        """
        Decode fractal pixel patterns back to binary data
        
        Args:
            frames: List of frame arrays
            
        Returns:
            Decoded binary data
        """
        bit_string = ""
        
        for frame in frames:
            chunk_bits = self._fractal_frame_to_bits(frame)
            bit_string += chunk_bits
        
        return self._parse_bit_string(bit_string)
    
    def _prepare_bit_string(self, data: bytes) -> str:
        """Prepare data with header containing metadata"""
        # Calculate CRC32 checksum
        checksum = zlib.crc32(data)
        
        # Create header: MAGIC + LENGTH + CHECKSUM + DATA
        magic = "FOLD"
        length = len(data)
        
        # Convert to binary strings
        magic_bits = ''.join(format(ord(c), '08b') for c in magic)
        length_bits = format(length, '032b')
        checksum_bits = format(checksum, '032b')
        data_bits = ''.join(format(b, '08b') for b in data)
        
        return magic_bits + length_bits + checksum_bits + data_bits
    
    def _parse_bit_string(self, bit_string: str) -> bytes:
        """Parse bit string back to data, validating checksum"""
        # Parse header
        magic_bits = bit_string[:32]  # 4 bytes
        length_bits = bit_string[32:64]  # 4 bytes
        checksum_bits = bit_string[64:96]  # 4 bytes
        data_bits = bit_string[96:]
        
        # Validate magic
        magic = ''.join(chr(int(magic_bits[i:i+8], 2)) for i in range(0, 32, 8))
        if magic != "FOLD":
            raise ValueError("Invalid FOLD file format")
        
        # Get length and validate
        length = int(length_bits, 2)
        expected_data_bits = length * 8
        
        if len(data_bits) < expected_data_bits:
            raise ValueError("Incomplete data")
        
        # Extract actual data
        actual_data_bits = data_bits[:expected_data_bits]
        data_bytes = bytes(int(actual_data_bits[i:i+8], 2) for i in range(0, len(actual_data_bits), 8))
        
        # Validate checksum
        calculated_checksum = zlib.crc32(data_bytes)
        expected_checksum = int(checksum_bits, 2)
        
        if calculated_checksum != expected_checksum:
            raise ValueError("Data corruption detected - checksum mismatch")
        
        return data_bytes
    
    def _bits_to_fractal_frame(self, bit_string: str) -> np.ndarray:
        """Convert bit string to frame (systematic bit mapping)"""
        # Pad bit string to fill frame
        total_bits = self.pixels_per_frame * 3
        padded_bits = bit_string.ljust(total_bits, '0')
        
        # Convert to pixel values (systematic mapping)
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        bit_index = 0
        for y in range(self.height):
            for x in range(self.width):
                # Take 3 consecutive bits for R,G,B
                if bit_index + 2 < len(padded_bits):
                    r_bit = padded_bits[bit_index]
                    g_bit = padded_bits[bit_index + 1]
                    b_bit = padded_bits[bit_index + 2]
                    
                    r = 255 if r_bit == '1' else 0
                    g = 255 if g_bit == '1' else 0
                    b = 255 if b_bit == '1' else 0
                    
                    frame[y, x] = [r, g, b]
                    bit_index += 3
                else:
                    # Fill remaining with black
                    frame[y, x] = [0, 0, 0]
        
        return frame
    
    def _fractal_frame_to_bits(self, frame: np.ndarray) -> str:
        """Convert frame back to bit string (systematic bit mapping)"""
        bit_string = ""
        
        for y in range(self.height):
            for x in range(self.width):
                # Extract RGB values and convert to bits
                r, g, b = frame[y, x]
                # Use consistent threshold for bit recovery
                r_bit = '1' if r >= 128 else '0'
                g_bit = '1' if g >= 128 else '0'
                b_bit = '1' if b >= 128 else '0'
                
                bit_string += r_bit + g_bit + b_bit
        
        return bit_string
    
    def _fractal_transform(self, x: int, y: int) -> Tuple[float, float]:
        """
        Apply fractal coordinate transformation
        Uses simplified Mandelbrot-like transformation
        """
        # Normalize coordinates
        nx = x / self.width
        ny = y / self.height
        
        # Apply non-linear transformation
        # This creates the "fractal" distribution pattern
        scale = 0.3
        cx = 0.1  # Center offset
        cy = 0.2
        
        # Mandelbrot-inspired transformation
        fx = nx + scale * np.sin(2 * np.pi * nx) * np.cos(2 * np.pi * ny) + cx
        fy = ny + scale * np.cos(2 * np.pi * nx) * np.sin(2 * np.pi * ny) + cy
        
        # Ensure values stay in [0,1] range
        fx = fx % 1.0
        fy = fy % 1.0
        
        return fx, fy

# Singleton instance for default use
_default_encoder = FractalEncoder()