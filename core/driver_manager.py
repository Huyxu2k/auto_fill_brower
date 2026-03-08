from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from loguru import logger
import os

class DriverManager:
    #OFILE_PATH = r"C:\Users\huynv\AppData\Local\Google\Chrome\User Data\Profile 2"
    PROFILE_PATH = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Profile 10"

    def __init__(self, profile_path: str | None = None):
        self.profile_path = profile_path or self.PROFILE_PATH
        self.headless = False
        self.driver = None  # Thêm biến để lưu trữ driver hiện tại

    def create_driver(self):
        options = Options()

        # dùng profile cố định nếu có
        if self.profile_path and os.path.exists(self.profile_path):
            logger.info(f"Sử dụng profile cố định: {self.profile_path}")
            options.add_argument(f"--user-data-dir={self.profile_path}")
        else:
            logger.warning("Không tìm thấy profile_path hoặc đường dẫn trống. Khởi tạo Chrome mới.")

        # Giữ trình duyệt mở sau khi script kết thúc
        options.add_experimental_option("detach", True)
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        if self.headless:
            options.add_argument("--headless=new")
        
        # tránh detect automation cơ bản
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(5)

        return driver

    def close():
        return