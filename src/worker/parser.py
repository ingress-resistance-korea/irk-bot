from typing import Type

from src.shared.type import IntelResult


def intel_result_to_dict(intel_result: Type[IntelResult]) -> dict:
    return {
        'success': intel_result.success,
        'address': intel_result.address,
        'start_time': intel_result.start_time,
        'timestamp': str(intel_result.timestamp),
        'url': intel_result.url,
        'error_message': intel_result.error_message,
    }
