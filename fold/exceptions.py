"""
Custom exceptions for FOLD library
"""

class FOLDException(Exception):
    """Base exception for all FOLD-related errors"""
    pass

class ValidationError(FOLDException):
    """Raised when input validation fails"""
    pass

class EncodingError(FOLDException):
    """Raised when encoding process fails"""
    pass

class DecodingError(FOLDException):
    """Raised when decoding process fails"""
    pass

class FileCorruptionError(FOLDException):
    """Raised when video file appears corrupted"""
    pass

class UnsupportedFormatError(FOLDException):
    """Raised when file format is not supported"""
    pass