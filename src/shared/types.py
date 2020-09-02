from dataclasses import dataclass
from datetime import datetime


@dataclass
class IntelResult:
    """Class for keeping track of an item in inventory."""
    success: bool
    address: str
    start_time: int
    timestamp: datetime
    url: str
    error_message: str
