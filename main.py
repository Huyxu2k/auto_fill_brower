from loguru import logger
from core.driver_manager import DriverManager
from core.reader_manager import ReaderManager
from pages.impl_page import TestPage
from models.person import Person


def main():
    #1. Đọc dữ liệu từ nguồn
    reader_manager = ReaderManager(r"C:\Users\huynv\Desktop\Test.xlsx")
    persons: list[Person] = reader_manager.read_excel()

    if len(persons) == 0:
        logger.info("Không có dữ liệu được load vào")
        return
    
    #2. Quản lý, tạo brower
    driver_manager = DriverManager()
    driver = driver_manager.create_driver()
    
    #3. Chạy test
    test_page = TestPage(driver)
    test_page.open()
    test_page.fill(persons[0])
    test_page.click_btn()
    #4. Loop

    logger.info(f"Hoàn thành !")
    
if __name__ == "__main__":
    main()