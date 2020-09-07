from enum import Enum

INTEL_REQUEST = 'intel_request'
INTEL_RESPONSE_TELEGRAM = 'intel_response_telegram'
INTEL_RESPONSE_SLACK = 'intel_response_slack'

INTEL_HELP_MESSAGE = '*/intel* 명령어 입력 후, 원하는 위치를 입력해주세요\n' \
                     'ex) `/intel 올림픽공원`'


class IntelRequestType(Enum):
    POSITION = 'position'
    LOCATION = 'location'
