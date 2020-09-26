from typing import Type

from src.shared.type import IntelResult


def parse_intel_result(result: dict) -> Type[IntelResult]:
    parsed_result = IntelResult

    parsed_result.success = result['success']
    parsed_result.file_url = result['file_url']
    parsed_result.file_path = result['file_path']
    parsed_result.address = result['address']
    parsed_result.error_message = result['error_message']
    parsed_result.timestamp = result['timestamp']
    parsed_result.intel_url = result['intel_url']
    parsed_result.location = result['location']
    return parsed_result

