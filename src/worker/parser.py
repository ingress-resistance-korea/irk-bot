from typing import Type

from src.shared.type import IntelResult
from src.shared.utils.datetime import get_timestamp


def intel_result_to_dict(intel_result: Type[IntelResult]) -> dict:
    return {
        'success': intel_result.success,
        'address': intel_result.address,
        'start_time': intel_result.start_time,
        'timestamp': get_timestamp(intel_result.timestamp),
        'url': intel_result.url,
        'error_message': intel_result.error_message,
        'intel_url': intel_result.intel_url,
        'location': {
            'lat': intel_result.location.latitude,
            'lon': intel_result.location.longitude,
        }
    }
