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
import json
from loguru import logger
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLineEdit, QTextEdit,
                            QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
                            QHeaderView, QCheckBox, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QObject


class LogHandler(QObject):
    # Đẩy log lên giao diện PyQt6
    n_log = pyqtSignal(str)

    def write(self, message : str):
        if message.strip():
            self.n_log.emit(message.strip())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Chrome")
        self.resize(1000, 600)
        self.init_ui()
        self.setup_logger()
        
    def setup_logger(self):
        # Tạo đối tượng handler
        self.log_handler = LogHandler()
        # Kết nối signal n_log tới hàm cập nhật UI
        self.log_handler.n_log.connect(self.update_log_ui)
        
        # Xóa các cấu hình logger mặc định cũ nếu có (vd log ra terminal) để tránh trùng lặp nếu ko cần
        logger.remove()
        
        # Thêm LogHandler vào loguru, cấu hình định dạng tùy chỉnh
        logger.add(self.log_handler, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        
        # Khởi tạo FormLayout để tự động căn lề thề hoàn hảo
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft) # Căn lề trái cho nhãn

        # 1. Chọn file Excel
        excel_container = QHBoxLayout()
        self.txt_file_path = QLineEdit()
        self.txt_file_path.setPlaceholderText("Đường dẫn file Excel dữ liệu...")
        self.txt_file_path.setReadOnly(True)
        btn_browse_excel = QPushButton("Chọn Excel")
        btn_browse_excel.clicked.connect(self.browse_file)
        excel_container.addWidget(self.txt_file_path)
        excel_container.addWidget(btn_browse_excel)
        form_layout.addRow("File Excel:", excel_container)

        # 2. Chọn Profile Chrome (Tùy chọn)
        profile_container = QHBoxLayout()
        self.chk_use_profile = QCheckBox("Profile")
        self.chk_use_profile.stateChanged.connect(self.toggle_profile_selection)
        
        self.txt_profile_path = QLineEdit()
        self.txt_profile_path.setPlaceholderText("Đường dẫn Profile Chrome...")
        self.txt_profile_path.setReadOnly(True)
        self.txt_profile_path.setEnabled(False) # Mặc định disable
        
        self.btn_browse_profile = QPushButton("Chọn Profile")
        self.btn_browse_profile.clicked.connect(self.browse_profile)
        self.btn_browse_profile.setEnabled(False) # Mặc định disable
        
        profile_container.addWidget(self.txt_profile_path)
        profile_container.addWidget(self.btn_browse_profile)
        form_layout.addRow(self.chk_use_profile, profile_container)
        
        # 3. Nhập URL
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("Nhập URL website điều khiển...")
        form_layout.addRow("URL Website:", self.txt_url)

        # 4. Chọn file JSON
        json_container = QHBoxLayout()
        self.txt_json_path = QLineEdit()
        self.txt_json_path.setPlaceholderText("Đường dẫn file JSON cấu hình bước...")
        self.txt_json_path.setReadOnly(True)
        btn_browse_json = QPushButton("Chọn JSON")
        btn_browse_json.clicked.connect(self.browse_json)
        json_container.addWidget(self.txt_json_path)
        json_container.addWidget(btn_browse_json)
        form_layout.addRow("File JSON:", json_container)
        
        # Thêm toàn bộ các trường nhập liệu trên vào Layout chính
        main_layout.addLayout(form_layout)

        
        # 5 & 6. Layout hiển thị JSON Steps và Log trực quan
        content_layout = QHBoxLayout()
        
        # Bảng hiển thị steps JSON
        steps_layout = QVBoxLayout()
        steps_layout.addWidget(QLabel("Các bước điều khiển (JSON):"))
        self.steps_table = QTableWidget()
        self.steps_table.setColumnCount(3)
        self.steps_table.setHorizontalHeaderLabels(["Action", "Locator", "Selector"])
        self.steps_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        steps_layout.addWidget(self.steps_table)
        content_layout.addLayout(steps_layout, 2) # Tỷ lệ 2
        
        # TextEdit hiển thị log
        log_layout = QVBoxLayout()
        log_layout.addWidget(QLabel("Log hệ thống:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        content_layout.addLayout(log_layout, 1) # Tỷ lệ 1
        
        main_layout.addLayout(content_layout)

        # Các nút điều khiển
        control_layout = QHBoxLayout()
        
        btn_start = QPushButton("Bắt đầu")
        btn_start.clicked.connect(self.start)
        btn_start.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        btn_stop = QPushButton("Dừng")
        btn_stop.clicked.connect(self.stop)
        btn_stop.setStyleSheet("background-color: #F44336; color: white; font-weight: bold;")
        
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_data)
        btn_clear.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        
        control_layout.addWidget(btn_start)
        control_layout.addWidget(btn_stop)
        control_layout.addWidget(btn_clear)
        
        main_layout.addLayout(control_layout)

    def toggle_profile_selection(self, state):
        is_checked = (state == Qt.CheckState.Checked.value)
        self.txt_profile_path.setEnabled(is_checked)
        self.btn_browse_profile.setEnabled(is_checked)
        if not is_checked:
            self.txt_profile_path.clear()

    def browse_profile(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục Profile Chrome")
        if dir_path:
            self.txt_profile_path.setText(dir_path)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file dữ liệu", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.txt_file_path.setText(file_path)

    def browse_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file JSON cấu hình", "", "JSON Files (*.json)")
        if file_path:
            self.txt_json_path.setText(file_path)
            self.load_json_steps(file_path)

    # TODO viết lại code để load steps từ file json và hiển thị lên giao diện, bao gồm trạng thái của 
    # từng bước đã thực hiện chưa
    def load_json_steps(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                steps = json.load(f)
            
            self.steps_table.setRowCount(0) # Clear bảng hiện tại
            
            if isinstance(steps, list):
                for i, step in enumerate(steps):
                    self.steps_table.insertRow(i)
                    self.steps_table.setItem(i, 0, QTableWidgetItem(str(step.get("action", ""))))
                    self.steps_table.setItem(i, 1, QTableWidgetItem(str(step.get("locator", ""))))
                    self.steps_table.setItem(i, 2, QTableWidgetItem(str(step.get("selector", ""))))
            elif isinstance(steps, dict):
                # Trường hợp file json chỉ có 1 dict
                self.steps_table.insertRow(0)
                self.steps_table.setItem(0, 0, QTableWidgetItem(str(steps.get("action", ""))))
                self.steps_table.setItem(0, 1, QTableWidgetItem(str(steps.get("locator", ""))))
                self.steps_table.setItem(0, 2, QTableWidgetItem(str(steps.get("selector", ""))))
                
            logger.info(f"Đã load thành công cấu hình JSON từ: {file_path}")
        except Exception as e:
            logger.error(f"Lỗi khi đọc file JSON: {str(e)}")

    def update_log_ui(self, message):
        self.log_output.append(message)
        # Tự động cuộn xuống cuối
        self.log_output.moveCursor(self.log_output.textCursor().MoveOperation.End)
    
    def start(self):
        logger.info("Bắt đầu chạy tool...")
        # TODO: Implement thêm logic gọi browser
        return
        
    def stop(self):
        logger.info("Đang dừng tiến trình...")
        # TODO: Implement logic dừng
        return
        
    def clear_data(self):
        self.txt_file_path.clear()
        self.chk_use_profile.setChecked(False)
        self.txt_profile_path.clear()
        self.txt_url.clear()
        self.txt_json_path.clear()
        self.steps_table.setRowCount(0)
        self.log_output.clear()
        logger.info("Đã xoá dữ liệu trên giao diện.")
    
    def run_process(self, path):
        return
    
if __name__ == "__main__":
    #main()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())