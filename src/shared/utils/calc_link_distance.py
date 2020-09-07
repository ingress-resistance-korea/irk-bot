from src.shared.constants import MOD_COMBINATIONS


def calculate_link_distance(resonators=None, mods=None):
    '''레저네이터, 모드 상태에 따른 링크거리를 알려드려요'''
    # check resonator
    reso_count = len(resonators)

    # reso count exception
    if reso_count != 8:
        text = '`8개의 레조네티어를 넣어주세요`'
        return text

    total_reso_level = 0
    for reso in resonators:
        try:
            lv_reso = int(reso)
        except:
            text = '`유효하지 않은 데이터입니다`'
            return text

        if lv_reso > 8 or lv_reso < 1:
            text = '`레조네이터의 레벨 범위는 1부터 8입니다`'
            return text
        else:
            total_reso_level += lv_reso

    # check mod
    if mods:
        try:
            mods = ''.join(sorted(mods.upper(), key=lambda m: {'V': 1, 'S': 2, 'R': 3}[m]))
            power_of_mods = MOD_COMBINATIONS[mods]
        except:
            text = '`모드가 잘못되었습니다.` (V,S,R 조합으로 최대 4개까지!)`'
            return text
    else:
        power_of_mods = 1

    # calc link distance
    distance = round(160 * ((total_reso_level / 8.0) ** 4) * power_of_mods, 3)

    # make message
    if distance > 1000:
        distance /= 1000
        text = '`%s km`' % distance
    else:
        text = '`%s m`' % distance
    return text
