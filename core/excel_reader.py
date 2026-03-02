import os
import pandas 
from loguru import logger

def read_excel(file_path):
    try:
        if not os.path.exists(file_path):
            logger.error(f"File {file_path} không tồn tại.")
            return []
        
        file = pandas.read_excel(file_path)

        if file.empty:
            logger.warning("File Excel không có dữ liệu")
            return []

    except Exception as ex:
        logger.exception("Lỗi khi đọc file Excel.") 
        return []