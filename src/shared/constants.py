from enum import Enum

INTEL_REQUEST = 'intel_request'
INTEL_RESPONSE_TELEGRAM = 'intel_response_telegram'
INTEL_RESPONSE_SLACK = 'intel_response_slack'


class IntelRequestType(Enum):
    POSITION = 'position'
    LOCATION = 'location'
