import time
import datetime

from src.worker.chromedriver import ChromeDriver
from src.shared.logger import getLogger
from src.worker.maps import get_location
from src.configs.settings import MAX_LOAD_TIME
from src.worker.constants import INTEL_URL, INTEL_TITLE
from src.worker.constatns_error import ADDRESS_NOT_FOUND_ERROR, INVALID_LOCATION_NAME_ERROR, \
    FAIL_TO_LOAD_INTEL_MAP_ERROR, FAIL_TO_LOAD_INTEL_MAP_DURING_LOADING_ERROR, \
    FAIL_TO_SAVE_SCREENSHOT_ERROR, TIME_EXCEED_ERROR

logger = getLogger()


class Crawler:
    def __init__(self, chrome: ChromeDriver):
        self.chrome = chrome
        self.start_time = None
        self.message = ''
        self.text = ''
        self.now = None

    def get_intel_screenshot(self, location_name: str) -> (bool, str):
        logger.info(location_name)
        self.start_time = int(time.time())
        self.now = datetime.datetime.now()

        # get response
        logger.info('[%s] Getting Address...' % (time.time() - self.start_time))
        address_data = get_location(location_name)
        if not len(address_data['results']):
            return False, ADDRESS_NOT_FOUND_ERROR

        # get address
        try:
            logger.info('[%s] Parsing Address...' % (time.time() - self.start_time))
            address = self._parse_address(address_data)
            lat, lng, width = self._get_geolocation(address_data)
            self.message = '%s\n' \
                           '%s' % (address, str(self.now))
        except Exception as e:
            logger.info(address_data)
            logger.info(e)
            return False, INVALID_LOCATION_NAME_ERROR

        # Settings Zoom Level
        logger.info('[%s] Setting Zoom Level...' % (time.time() - self.start_time))
        z = self._get_zoom_level(width)

        # Getting Intel Map
        logger.info('[%s] Getting Intel Map...' % (time.time() - self.start_time))
        if not self._get_intel_map(lat=lat, lng=lng, z=z) or not self._check_intel_map_loaded():
            self.text = FAIL_TO_LOAD_INTEL_MAP_ERROR
            return False, self.text

        logger.info('[%s] %s (lat: %s, lng: %s, z: %s)' % ((time.time() - self.start_time), location_name, lat, lng, z))
        if not self._load_intel_map():
            self.text = FAIL_TO_LOAD_INTEL_MAP_DURING_LOADING_ERROR
            return False, self.text

        # Saving Screenshot
        logger.info('[%s] Saving Screenshot...' % (time.time() - self.start_time))
        if not self._save_screenshot():
            self.text = FAIL_TO_SAVE_SCREENSHOT_ERROR
            return False, self.text
        return True, self.text

    @staticmethod
    def _get_zoom_level(width: float) -> int:
        all_portal_zoom = 0.08
        if width < all_portal_zoom:
            z = 15
        else:
            z = 13
            extra_z = 0
            while width > all_portal_zoom * (2 ** (2 + extra_z)):
                extra_z += 1
            z -= extra_z
        return z

    @staticmethod
    def _parse_address(address_data) -> str:
        return address_data['results'][0]['formatted_address']

    @staticmethod
    def _get_geolocation(address_data) -> (float, float, float):
        lat = round(float(address_data['results'][0]['geometry']['location']['lat']), 6)
        lng = round(float(address_data['results'][0]['geometry']['location']['lng']), 6)
        edge_west = address_data['results'][0]['geometry']['viewport']['southwest']['lng']
        edge_east = address_data['results'][0]['geometry']['viewport']['northeast']['lng']
        width = edge_east - edge_west
        return lat, lng, width

    def _get_intel_map(self, lat, lng, z) -> bool:
        url = INTEL_URL % (lat, lng, z)
        logger.info(url)
        try:
            self.chrome.driver.get(url)
            time.sleep(1)
        except Exception as e:
            logger.info(e)
            return False
        return True

    def _check_intel_map_loaded(self) -> bool:
        return self.chrome.driver.title == INTEL_TITLE

    def _load_intel_map(self) -> bool:
        while True:
            current_time = int(time.time())
            spent_time = current_time - self.start_time

            # Timeout
            if spent_time > MAX_LOAD_TIME:
                self.message = '%s\n' \
                               '%s' % (TIME_EXCEED_ERROR, self.message)
                return True

            # Get Loading Percent
            try:
                loading_msg = self.chrome.driver.find_element_by_id('loading_msg')
            except Exception as e:
                logger.info(e)
                logger.info(self.chrome.driver.page_source)
                return False

            # Load Complete
            if loading_msg.get_attribute("style") == 'display: none;':
                return True
            time.sleep(1)

    def _save_screenshot(self):
        filename = self.now.strftime('%Y%m%d%H%M%S')
        try:
            file_url = self.chrome.save_screenshot(filename)
            self.text = '%s\n%s' % (self.message, file_url)
        except Exception as e:
            logger.info(e)
            return False
        return True
