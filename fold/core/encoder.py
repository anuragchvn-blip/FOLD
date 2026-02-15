"""
Core encoder for FOLD - converts data to video
"""

import cv2
import numpy as np
from typing import Union, Optional
import os
import time
from tqdm import tqdm

from .fractal import FractalEncoder, _default_encoder
from ..utils.validation import validate_input_data, validate_output_path
from ..utils.logging import setup_logger, log_performance
from ..exceptions import EncodingError

logger = setup_logger("fold.encoder")

def store(data: Union[str, bytes, bytearray], 
          output_path: Optional[str] = None,
          fps: int = 30,
          width: int = 1920,
          height: int = 1080) -> str:
    """
    Convert data to video file using fractal encoding
    
    Args:
        data: Input data (string, bytes, or bytearray)
        output_path: Output video file path (optional)
        fps: Frames per second
        width: Video width
        height: Video height
        
    Returns:
        str: Path to created video file
        
    Raises:
        EncodingError: If encoding fails
    """
    start_time = time.time()
    try:
        # Validate and prepare input
        logger.info("Starting encoding process...")
        byte_data = validate_input_data(data)
        logger.info(f"Input data size: {len(byte_data)} bytes")
        
        # Generate output path if not provided
        if output_path is None:
            output_path = _generate_output_path(byte_data)
        
        output_path = validate_output_path(output_path)
        
        # Create fractal encoder
        encoder = FractalEncoder(width, height)
        
        # Encode data to frames
        logger.info("Encoding data to fractal frames...")
        frames = list(encoder.encode_data_to_pixels(byte_data))
        logger.info(f"Generated {len(frames)} frames")
        
        # Write video file
        logger.info(f"Writing video to {output_path}")
        _write_video(frames, output_path, fps, width, height)
        
        # Log performance
        exec_time = time.time() - start_time
        log_performance(logger, "Encoding", exec_time, len(byte_data))
        logger.info(f"Video saved to: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Encoding failed: {str(e)}")
        raise EncodingError(f"Failed to encode data: {str(e)}") from e

def _generate_output_path(data: bytes) -> str:
    """Generate default output path based on data"""
    import hashlib
    import time
    
    # Create hash of data for unique filename
    data_hash = hashlib.md5(data).hexdigest()[:8]
    timestamp = int(time.time())
    
    filename = f"fold_{data_hash}_{timestamp}.mp4"
    return os.path.join(os.getcwd(), filename)

def _write_video(frames: list, output_path: str, fps: int, width: int, height: int):
    """Write frames to video file using lossless codec"""
    try:
        # Use AVI container with uncompressed codec for lossless
        # OpenCV works best with AVI for raw/lossless video
        avi_path = output_path.replace('.mp4', '.avi') if output_path.endswith('.mp4') else output_path
        if not avi_path.endswith('.avi'):
            avi_path = avi_path + '.avi'
        
        # Use uncompressed RGBA codec - truly lossless
        fourcc = cv2.VideoWriter_fourcc(*'RGBA')
        video_writer = cv2.VideoWriter(avi_path, fourcc, fps, (width, height))
        
        if not video_writer.isOpened():
            raise EncodingError("Failed to initialize video writer")
        
        # Write frames with progress bar
        for frame in tqdm(frames, desc="Writing frames", unit="frame"):
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video_writer.write(frame_bgr)
        
        video_writer.release()
        
        # Verify file was created
        if not os.path.exists(avi_path):
            raise EncodingError("Video file was not created")
        
        # Rename to .mp4 if requested
        if output_path.endswith('.mp4') and avi_path != output_path:
            import shutil
            shutil.move(avi_path, output_path)
        else:
            output_path = avi_path
        
        logger.info(f"Video file size: {os.path.getsize(output_path)} bytes")
        
    except Exception as e:
        raise EncodingError(f"Failed to write video: {str(e)}") from e