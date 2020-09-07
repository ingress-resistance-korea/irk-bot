from enum import Enum

INTEL_REQUEST = 'intel_request'
INTEL_RESPONSE_TELEGRAM = 'intel_response_telegram'
INTEL_RESPONSE_SLACK = 'intel_response_slack'


class IntelRequestType(Enum):
    POSITION = 'position'
    LOCATION = 'location'


MOD_COMBINATIONS = {
    '': 1.000,
    'R': 2.000,
    'RR': 2.500,
    'RRR': 2.750,
    'RRRR': 3.000,
    'S': 5.000,
    'SR': 5.500,
    'SRR': 5.750,
    'SRRR': 6.000,
    'SS': 6.250,
    'SSR': 6.500,
    'SSRR': 6.750,
    'SSS': 6.825,
    'SSSR': 7.125,
    'SSSS': 7.500,
    'V': 7.000,
    'VR': 7.500,
    'VRR': 7.750,
    'VRRR': 8.000,
    'VS': 8.250,
    'VSR': 8.500,
    'VSRR': 8.750,
    'VSS': 8.875,
    'VSSR': 9.125,
    'VSSS': 9.500,
    'VV': 8.750,
    'VVR': 9.000,
    'VVRR': 9.250,
    'VVS': 9.375,
    'VVSR': 9.625,
    'VVSS': 10.000,
    'VVV': 9.625,
    'VVVR': 9.875,
    'VVVS': 10.250,
    'VVVV': 10.500,
}
