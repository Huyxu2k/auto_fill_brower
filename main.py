from loguru import logger
from core.driver_manager import DriverManager
from core.reader_manager import ReaderManager
from pages.impl_page import TestPage
from models.person import Person


def main():
    #1. Đọc dữ liệu từ nguồn
    reader_manager = ReaderManager(r"C:\Users\Admin\Desktop\test.xlsx")
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
    test_page.wait(5)
    test_page.fill(persons[0])
    test_page.wait(5)
    test_page.click_btn()
    #4. Loop

    logger.info(f"Hoàn thành !")


# giao diện 

import sys
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLineEdit, QTextEdit,
                            QLabel, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QObject


class LogHandler(QObject):
    # Đẩy log lên giao diện PyQt6
    n_log = pyqtSignal(str)

    def write(self, message):
        if message.strip():
            self.n_log.emit(message.strip())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
    def init_ui(self):
       #TODO
       return 
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file dữ liệu", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.txt_file_path.setText(file_path)

    def update_log_ui(self, message):
        self.log_output.append(message)
        # Tự động cuộn xuống cuối
        self.log_output.moveCursor(self.log_output.textCursor().MoveOperation.End)
    
    def start(self):
        return
    
    def run_process(self, path):
        return
    
if __name__ == "__main__":
    #main()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())