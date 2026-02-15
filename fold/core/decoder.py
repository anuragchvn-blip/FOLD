"""
Core decoder for FOLD - converts video back to data
"""

import cv2
import numpy as np
from typing import Union
import os
import time

from .fractal import FractalEncoder, _default_encoder
from ..utils.validation import validate_file_path
from ..utils.logging import setup_logger, log_performance
from ..exceptions import DecodingError, FileCorruptionError

logger = setup_logger("fold.decoder")

def retrieve(video_path: str) -> bytes:
    """
    Convert video file back to original data using fractal decoding
    
    Args:
        video_path: Path to video file
        
    Returns:
        bytes: Original data
        
    Raises:
        DecodingError: If decoding fails
        FileCorruptionError: If video appears corrupted
    """
    start_time = time.time()
    try:
        # Validate input file
        logger.info("Starting decoding process...")
        video_path = validate_file_path(video_path)
        file_size = os.path.getsize(video_path)
        logger.info(f"Input video size: {file_size} bytes")
        
        # Read video frames
        logger.info("Reading video frames...")
        frames = _read_video_frames(video_path)
        logger.info(f"Read {len(frames)} frames")
        
        if not frames:
            raise FileCorruptionError("No frames found in video")
        
        # Get video dimensions
        height, width = frames[0].shape[:2]
        
        # Create fractal decoder
        decoder = FractalEncoder(width, height)
        
        # Decode frames to data
        logger.info("Decoding fractal frames to data...")
        try:
            data = decoder.decode_pixels_to_data(frames)
            logger.info(f"Recovered data size: {len(data)} bytes")
        except ValueError as e:
            raise FileCorruptionError(f"Data corruption detected: {str(e)}")
        
        # Log performance
        exec_time = time.time() - start_time
        log_performance(logger, "Decoding", exec_time, len(data))
        
        return data
        
    except FileCorruptionError:
        raise
    except Exception as e:
        logger.error(f"Decoding failed: {str(e)}")
        raise DecodingError(f"Failed to decode video: {str(e)}") from e

def _read_video_frames(video_path: str) -> list:
    """Read all frames from video file"""
    try:
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise DecodingError("Failed to open video file")
        
        frames = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
            frame_count += 1
            
            # Progress logging for large videos
            if frame_count % 100 == 0:
                logger.debug(f"Read {frame_count} frames...")
        
        cap.release()
        
        if not frames:
            raise FileCorruptionError("Video contains no decodable frames")
            
        return frames
        
    except Exception as e:
        raise DecodingError(f"Failed to read video frames: {str(e)}") from e