import os
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.webdriver import WebDriver

from src.configs.settings import GOOGLE_EMAIL, GOOGLE_PASSWORD, INGRESS_AGENT_NAME
from src.configs.settings import CHROMEDRIVER_PATH, SCREENSHOT_DIR, SERVER_URL
from src.worker.constants import ACCOUNTS_GOOGLE_COM, INTEL_INGRESS_COM, EMAIL, SIGN_IN, PASSWORD, SUBMIT, \
    SUBMIT_APPROVE_ACCESS, LOGIN


def setup_chrome() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("%s" % CHROMEDRIVER_PATH, chrome_options=chrome_options)
    return driver


class ChromeDriver:
    driver = None
    origin_bounding_box = (20, 151, 1845, 897)

    def __init__(self, logger):
        self.logger = logger
        self.logger.info('Initialize ChromeDriver Start...')
        self.driver = setup_chrome()
        self.driver = self.sign_in_google_from_intel_map()
        self.logger.info('Initialize ChromeDriver Complete...')

    def save_screenshot(self, filename):
        file_dir = SCREENSHOT_DIR
        png_file_path = file_dir + '/' + filename + '.png'
        # jpg_file_path = file_dir + '/' + filename + '.jpg'
        self.driver.save_screenshot(png_file_path)
        base_image = Image.open(png_file_path)
        cropped_image = base_image.crop(self.origin_bounding_box)
        cropped_image.save(png_file_path)
        # rgb_im = cropped_image.convert('RGB')
        # rgb_im.save(jpg_file_path)
        # file_url = SERVER_URL + '/screenshots/' + filename + '.png'
        file_url = SCREENSHOT_DIR + '/' + filename + '.png'
        # try:
        #     os.remove(png_file_path)
        # except Exception as e:
        #     print(e)
        #     pass
        return file_url

    def sign_in_google_from_intel_map(self) -> WebDriver:
        self.logger.info('Signing In Google From Intel Map...')
        url = 'https://%s' % INTEL_INGRESS_COM
        google_sign_in_url = None
        self.driver.get(url)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        a_tags = soup.find_all('a')
        for a_tag in a_tags:
            href = a_tag.get('href')
            if href.find(ACCOUNTS_GOOGLE_COM) and href.find(INTEL_INGRESS_COM):
                google_sign_in_url = href
                self.logger.info(google_sign_in_url)
                break

        if not google_sign_in_url:
            raise ValueError

        self.driver.delete_all_cookies()
        self.driver.get(google_sign_in_url)
        sleep(1)
        try:
            self.driver.find_element_by_name(EMAIL).send_keys(GOOGLE_EMAIL)
        except:
            print(self.driver.page_source)
            self.save_screenshot(EMAIL)
        self.driver.find_element_by_name(SIGN_IN).click()
        sleep(1)
        try:
            self.driver.find_element_by_name(PASSWORD).send_keys(GOOGLE_PASSWORD)
        except:
            self.save_screenshot(PASSWORD)
            print(self.driver.page_source)
        try:
            self.driver.find_element_by_id(SUBMIT).click()
        except:
            self.save_screenshot('signIn2')
            print(self.driver.page_source)
        sleep(1)
        try:
            self.driver.find_element_by_id(SUBMIT_APPROVE_ACCESS).click()
        except:
            print(self.driver.page_source)
            self.save_screenshot(LOGIN)
        sleep(1)
        # Check Success
        cnt = 0
        self.logger.info('Finding Agent Name from Page Source...')
        while self.driver.page_source.find(INGRESS_AGENT_NAME) == -1:
            sleep(1)
            self.logger.info('Try Again...')
            cnt += 1
            if cnt > 10:
                print(self.driver.page_source)
                raise PermissionError
        self.logger.info('Sign In Google Complete!!!')
        sleep(1)
        return self.driver
