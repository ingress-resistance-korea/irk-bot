import time
import datetime
from uuid import uuid4

from src.worker.chromedriver import ChromeDriver
from src.utils.logger import getLogger
from src.utils.maps import get_location
from src.config.settings import MAX_LOAD_TIME

logger = getLogger()


def get_intel_screenshot(chrome: ChromeDriver, search_key):
    start_time = int(time.time())
    logger.info(search_key)
    now = datetime.datetime.now()

    if not chrome.check_lock():
        lock_id = uuid4()
        if not (chrome.lock(lock_id=lock_id)):
            text = '`%s에 사용을 시작한 유저가 있습니다. 잠시만 기다려주세요`' % chrome.locked_at
            return False, text
    else:
        text = '`%s에 사용을 시작한 유저가 있습니다. 잠시만 기다려주세요`' % chrome.locked_at
        return False, text

    # get response
    logger.info('[%s] Getting Geolocation...' % (time.time() - start_time))
    data = get_location(search_key)
    if not len(data['results']):
        text = '`구글에 주소 데이터가 없습니다.`'
        chrome.unlock()
        return False, text

    # get address
    try:
        logger.info('[%s] Finding Address...' % (time.time() - start_time))
        address = data['results'][0]['formatted_address']
        message = '%s\n' \
                  '`%s`' % (address, str(now))
    except Exception as e:
        logger.info(e)
        logger.info(data)
        text = '`주소를 불러오는데 실패했습니다.`\n' \
               '>%s' % search_key
        chrome.unlock()
        return False, text

    # parsing address
    try:
        logger.info('[%s] Parsing Address...' % (time.time() - start_time))
        lat = round(float(data['results'][0]['geometry']['location']['lat']), 6)
        lng = round(float(data['results'][0]['geometry']['location']['lng']), 6)
        edge_west = data['results'][0]['geometry']['viewport']['southwest']['lng']
        edge_east = data['results'][0]['geometry']['viewport']['northeast']['lng']
        width = edge_east - edge_west

    except Exception as e:
        logger.info(e)
        logger.info(data)
        text = '`좌표를 불러오는데 실패했습니다.`\n' \
               '>%s' % address
        chrome.unlock()
        return False, text

    # Settings Zoom Level
    logger.info('[%s] Setting Zoom Level...' % (time.time() - start_time))
    all_portal_zoom = 0.08
    if width < all_portal_zoom:
        z = 15
    else:
        z = 13
        extra_z = 0
        while width > all_portal_zoom * (2 ** (2 + extra_z)):
            extra_z += 1
        z -= extra_z

    # Getting Intel Map
    logger.info('[%s] Getting Intel Map...' % (time.time() - start_time))
    url = 'https://intel.ingress.com/intel?ll=%s,%s&z=%s' % (lat, lng, z)
    logger.info(url)
    chrome.driver.get(url)
    time.sleep(1)

    logger.info('[%s] %s (lat: %s, lng: %s, z: %s)' % ((time.time() - start_time), search_key, lat, lng, z))
    if chrome.driver.title != 'Ingress Intel Map':
        text = '지도를 불러오는 데 실패했어요 ㅠㅠ'
        chrome.unlock()
        return False, text

    while True:
        current_time = int(time.time())
        spent_time = current_time - start_time

        # Timeout
        if spent_time > MAX_LOAD_TIME:
            message = '너무 오래걸리는 지역이라서 이정도만 보여드릴게요!\n' \
                      '%s' % message
            break

        # Get Loading Percent
        try:
            loading_msg = chrome.driver.find_element_by_id('loading_msg')
        except Exception as e:
            logger.info(e)
            logger.info(chrome.driver.page_source)
            text = '지도를 불러오긴 했는데... 로딩하는 도중에 실패했어요 ㅠㅠ'
            chrome.unlock()
            return False, text

        # Load Complete
        if loading_msg.get_attribute("style") == 'display: none;':
            break
        time.sleep(1)

    # Saving Screenshot
    logger.info('[%s] Saving Screenshot...' % (time.time() - start_time))
    filename = now.strftime('%Y%m%d%H%M%S')
    try:
        file_url = chrome.save_screenshot(filename)
        text = '%s\n%s' % (message, file_url)
    except Exception as e:
        text = '스크린샷 저장에 실패했어요... ㅠㅠ'
        logger.info(e)
        return False, text

    chrome.unlock()
    return True, text
