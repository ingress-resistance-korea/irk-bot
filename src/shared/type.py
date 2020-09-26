from dataclasses import dataclass
from datetime import datetime
from typing import Type


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class IntelResult:
    """Class for keeping track of an item in inventory."""
    success: bool
    address: str
    start_time: int
    timestamp: datetime
    file_url: str
    file_path: str
    error_message: str
    intel_url: str
    location: Type[Location]
