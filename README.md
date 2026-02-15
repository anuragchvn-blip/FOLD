# FOLD - Fractal Optimized Layered Data

FOLD is a data-to-video encoding system that converts arbitrary files (JSON, code, text, images, binary data) into video files using fractal pixel encoding, enabling lossless data retrieval from the resulting video.

## Use Case

**Problem:** Data needs to be stored or transmitted in a format that appears as ordinary video media.

**Solution:** FOLD encodes any data type into video frames using fractal pixel patterns, preserving the original data bit-for-bit. The encoded video plays as normal video while containing hidden data that can be extracted losslessly.

**Applications:**
- Steganography and covert data transmission
- Data archival in video format
- Bypass media-only data transfer restrictions
- Unique data packaging for creative/technical projects

## What It Does

FOLD provides two core functions:

1. **Encode (`store`)**: Convert any file or byte data into a video file
2. **Decode (`retrieve`)**: Extract the original data from the video file

The system automatically:
- Generates fractal-encoded pixel patterns from input data
- Embeds CRC32 checksums for integrity verification
- Supports any file type (JSON, code, images, text, binary)

## How It Works

### Encoding Process

```
Input Data → Bit String → Fractal Frames → Video File
              (with header)   (RGB pixels)    (.avi/.mp4)
```

1. **Data Preparation**: Input is converted to bytes with header (magic + length + checksum)
2. **Bit Encoding**: Each bit becomes RGB pixel values (threshold at 128)
3. **Frame Generation**: Pixels are arranged into video frames
4. **Video Output**: Frames written as uncompressed AVI video

### Decoding Process

```
Video File → Frames → Pixel Values → Bit String → Original Data
                          (threshold)    (with header)   (verified)
```

1. **Frame Reading**: Video frames are read as RGB arrays
2. **Bit Recovery**: Pixel values converted back to bits using threshold
3. **Data Parsing**: Header extracted, checksum verified, data returned

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from fold import store, retrieve

# Encode a file to video
video_path = store("data.json", "output.avi")

# Decode video back to original data
original_data = retrieve("output.avi")
```

### SDK Usage

```python
from fold_sdk import FoldMemory

# Initialize memory storage
memory = FoldMemory("./storage")

# Add file (encodes to video)
mp4_path = memory.add_file("config.json")

# Search for files
results = memory.search("config")

# Decode video to original data
data = memory.decode(mp4_path)
```

### API Server

```bash
# Start the REST API
python -m fold.api.server

# Or run with uvicorn
uvicorn fold.api.server:app --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service status |
| GET | `/files` | List all stored files |
| POST | `/encode` | Upload and encode file |
| POST | `/search` | Search stored files |
| GET | `/decode/{filename}` | Decode and retrieve file |
| POST | `/batch_encode` | Encode multiple files |
| DELETE | `/files/{filename}` | Delete stored file |

## Product Requirements Document (PRD)

### Core Features

#### F1: Data Encoding
- **Requirement**: Encode any file type to video format
- **Input**: File path or byte data
- **Output**: AVI video file
- **Validation**: CRC32 checksum embedded in output

#### F2: Data Decoding
- **Requirement**: Decode video back to original data losslessly
- **Input**: Video file path
- **Output**: Original byte data
- **Validation**: CRC32 verification before returning

#### F3: Format Support
- **Requirement**: Support JSON, text, code, images, binary
- **Detection**: Automatic file type detection via content analysis

#### F4: Metadata Management (AI Memory System)
- **Requirement**: Extract, inject, and search metadata
- **Features**: Keywords, summary, file type, hash, timestamps

#### F5: Search Indexing
- **Requirement**: In-memory index of all stored videos
- **Capabilities**: Keyword search, exact/partial matching

#### F6: REST API
- **Requirement**: HTTP interface for remote operations
- **Authentication**: None (internal use)

### Non-Functional Requirements

#### Performance
- Encode: <2s per file (small files)
- Decode: <1s per file (small files)
- Search: <50ms latency

#### Data Integrity
- Lossless encoding/decoding verified via CRC32
- SHA256 hash tracking for verification

#### Compatibility
- Output: AVI container with RGBA codec
- Tested on Windows

### Architecture

```
fold/
├── core/           # Encoder/Decoder
│   ├── encoder.py  # Data → Video
│   ├── decoder.py  # Video → Data
│   └── fractal.py  # Fractal encoding logic
├── ai/             # AI Memory System
│   ├── metadata.py # Metadata extraction/injection
│   ├── indexer.py  # Search index
│   └── search.py   # Search engine
├── sdk/            # Python SDK
│   └── python/
│       └── fold_sdk.py
├── api/            # REST API
│   └── server.py
└── cli/            # Command-line
    └── main.py
```

## License

Proprietary - All rights reserved.
