from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class DriverManager:
    PROFILE_PATH = r"C:\Users\huynv\AppData\Local\Google\Chrome\User Data\Profile 2"

    def __init__(self, profile_path: str | None = None):
        self.profile_path = profile_path or self.PROFILE_PATH
        self.headless = False

    def create_driver(self):
        options = Options()

        # dùng profile cố định
        options.add_argument(f"--user-data-dir={self.profile_path}")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        if self.headless:
            options.add_argument("--headless=new")
        
        # tránh detect automation cơ bản
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service()

        driver = webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(5)

        return driver
