from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class DriverManager:
    PROFILE_PATH = r""

    @staticmethod
    def init_brower(headless = False):
        options = Options()

        # dùng profile cố định
        options.add_argument(f"--user-data-dir={DriverManager.PROFILE_PATH}")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        if headless:
            options.add_argument("--headless=new")
        
        # tránh detect automation cơ bản
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(5)

        return driver