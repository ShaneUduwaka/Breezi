# audio/audio_buffer.py
"""
Audio buffer with jitter handling for real-time streaming
Handles timing issues and maintains audio quality
"""

import asyncio
from collections import deque
from typing import Optional
from dataclasses import dataclass
import time


@dataclass
class AudioFrame:
    """Represents a single audio frame"""
    data: bytes
    sample_rate: int = 16000
    channels: int = 1
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def duration_ms(self) -> float:
        """Calculate frame duration in milliseconds"""
        # bytes / (sample_rate * channels * 2 bytes per sample) * 1000
        samples = len(self.data) // (self.channels * 2)
        return (samples / self.sample_rate) * 1000


class AudioBuffer:
    """
    Manages audio buffering with jitter handling
    Maintains optimal buffer size for real-time streaming
    """
    
    def __init__(self, buffer_size_ms: int = 250, sample_rate: int = 16000):
        """
        Initialize audio buffer
        
        Args:
            buffer_size_ms: Target buffer size in milliseconds
            sample_rate: Audio sample rate (Hz)
        """
        self.buffer_size_ms = buffer_size_ms
        self.sample_rate = sample_rate
        
        # Calculate target buffer size in bytes
        # 250ms at 16kHz stereo = 16000 * 0.25 * 2 bytes = 8000 bytes
        self.target_buffer_bytes = int(sample_rate * (buffer_size_ms / 1000) * 2)
        
        self.frames: deque[AudioFrame] = deque()
        self.total_bytes = 0
        self.lock = asyncio.Lock()
    
    async def add_frame(self, frame: AudioFrame):
        """Add audio frame to buffer"""
        async with self.lock:
            self.frames.append(frame)
            self.total_bytes += len(frame.data)
    
    async def get_frame(self) -> Optional[AudioFrame]:
        """Get next audio frame from buffer"""
        async with self.lock:
            if self.frames:
                frame = self.frames.popleft()
                self.total_bytes -= len(frame.data)
                return frame
        return None
    
    async def peek(self) -> Optional[AudioFrame]:
        """Peek at next frame without removing"""
        async with self.lock:
            if self.frames:
                return self.frames[0]
        return None
    
    async def is_ready(self) -> bool:
        """
        Check if buffer has enough data
        Ready when buffer is at least 1/2 of target size
        """
        async with self.lock:
            return self.total_bytes >= (self.target_buffer_bytes // 2)
    
    async def is_full(self) -> bool:
        """Check if buffer is full"""
        async with self.lock:
            return self.total_bytes >= self.target_buffer_bytes
    
    async def clear(self):
        """Clear all buffered frames"""
        async with self.lock:
            self.frames.clear()
            self.total_bytes = 0
    
    async def buffer_size_ms(self) -> float:
        """Get current buffer size in milliseconds"""
        async with self.lock:
            if not self.frames:
                return 0
            
            total_ms = sum(frame.duration_ms() for frame in self.frames)
            return total_ms
    
    def get_stats(self) -> dict:
        """Get buffer statistics"""
        return {
            "total_bytes": self.total_bytes,
            "target_bytes": self.target_buffer_bytes,
            "frame_count": len(self.frames),
            "fullness_percent": (self.total_bytes / self.target_buffer_bytes) * 100
        }
