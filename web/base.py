from abc import ABC, abstractmethod
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
import os
from datetime import datetime

class BaseForm(ABC):
    # -------------------------
    # CONST
    # -------------------------
    DEFAULT_TIMEOUT = 10
    LOADING_SPINNER = (By.CSS_SELECTOR, '[title="Loading..."]')
    SCREENSHOT_FOLDER = "screenshots"

    def __init__(self, browser, timeout = DEFAULT_TIMEOUT):
        self.browser = browser
        self.timeout = timeout
        #self._create_screenshot_folder()
    
    # -------------------------
    # SETUP
    # -------------------------

    def screenshot_folder(self):
        if not os.path.exists(self.SCREENSHOT_FOLDER):
            os.makedirs(self.SCREENSHOT_FOLDER)

    # -------------------------
    # UTILITY
    # -------------------------

    def take_screenshot(self, name_prefix="error"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.SCREENSHOT_FOLDER}/{name_prefix}_{timestamp}.png"
        self.browser.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")

    def _handle_exception(self, message, exception):
        logger.error(message)
        self.take_screenshot("failure")
        raise exception

    # -------------------------
    # WAIT METHODS
    # -------------------------

    def wait_until_visible(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            logger.info(f"Waiting for element visible: {locator}")
            return WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException as e:
            self._handle_exception(
                f"Element not visible after {timeout}s: {locator}", e
            )

    def wait_until_clickable(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            logger.info(f"Waiting for element clickable: {locator}")
            return WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException as e:
            self._handle_exception(
                f"Element not clickable after {timeout}s: {locator}", e
            )

    def wait_until_invisible(self, locator, timeout=None):
        timeout = timeout or self.timeout
        try:
            logger.info(f"Waiting for element invisible: {locator}")
            WebDriverWait(self.browser, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException as e:
            self._handle_exception(
                f"Element still visible after {timeout}s: {locator}", e
            )


    # -------------------------
    # ACTION METHODS
    # -------------------------

    def get(self, locator):
        return self.wait_until_visible(locator)

    def click(self, locator):
        try:
            element = self.wait_until_clickable(locator)
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            self._handle_exception(f"Failed clicking element: {locator}", e)

    def get_multiple(self, locator):
        logger.info(f"Finding multiple elements: {locator}")
        return self.browser.find_elements(*locator)

    def contains(self, text):
        safe_text = text.replace('"', '\\"')
        locator = (By.XPATH, f'//*[contains(text(), "{safe_text}")]')
        return self.wait_until_visible(locator)

    def find_element_by_text(self, elements, text):
        logger.info(f"Searching for text '{text}' in elements")
        for element in elements:
            if text.lower() in element.text.lower():
                return element

        error = NoSuchElementException(f'Element containing "{text}" not found')
        self._handle_exception(str(error), error)

    def get_nth_of_elements(self, nth, locator):
        elements = self.get_multiple(locator)

        if nth <= 0 or nth > len(elements):
            error = IndexError(
                f"Invalid index {nth}. Only {len(elements)} elements found"
            )
            self._handle_exception(str(error), error)

        return elements[nth - 1]

    # -------------------------
    # SPINNER
    # -------------------------

    def wait_for_loading_spinner(self):
        try:
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located(self.LOADING_SPINNER)
            )
        except TimeoutException:
            return

        self.wait_until_invisible(self.LOADING_SPINNER)

    
    def submit_and_wait(
        self,
        button_locator,
        success_locator=None,
        success_text=None,
        wait_url_change=False,
        timeout=None
    ):
        timeout = timeout or self.timeout
        old_url = self.browser.current_url

        try:
            logger.info(f"Submitting form using button: {button_locator}")
            self.wait_until_clickable(button_locator).click()

            # nếu có spinner thì chờ spinner
            self.wait_for_loading_spinner()

            # 1️⃣ chờ URL thay đổi
            if wait_url_change:
                logger.info("Waiting for URL change...")
                WebDriverWait(self.browser, timeout).until(
                    EC.url_changes(old_url)
                )

            # 2️⃣ chờ element thành công
            if success_locator:
                logger.info(f"Waiting for success element: {success_locator}")
                WebDriverWait(self.browser, timeout).until(
                    EC.visibility_of_element_located(success_locator)
                )

            # 3️⃣ chờ text thành công
            if success_text:
                logger.info(f"Waiting for success text: {success_text}")
                WebDriverWait(self.browser, timeout).until(
                    EC.text_to_be_present_in_element(
                        (By.TAG_NAME, "body"), success_text
                    )
                )

            logger.info("Submit successful.")

        except TimeoutException as e:
            self._handle_exception("Submit failed or success condition not met", e)

    # -------------------------
    # AbstractCTION METHODS
    # -------------------------

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def fill(self, data: dict):
        pass

    @abstractmethod
    def submit(self):
        pass