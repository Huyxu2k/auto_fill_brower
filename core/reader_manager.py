import os
import pandas 
from loguru import logger

class ReaderManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def validate(self):
        if not self.file_path:
            logger.error(f"Đường dẫn file rỗng.")
            return False
        if not os.path.exists(self.file_path):
            logger.error(f"File {self.file_path} không tồn tại.")
            return False
        if not self.file_path.endswith((".xlsx", ".xls")):
            logger.error(f"File không đúng định dạng Excel.")
            return False
        return True
            

    def read_excel(self):
        try:
            if not self.validate():
                return []
            
            data = pandas.read_excel(self.file_path)

            if data.empty:
                logger.warning(f"File Excel không có dữ liệu")
                return []
            
            return data.to_dict(orient="records")

        except Exception as ex:
            logger.exception(f"Lỗi khi đọc file Excel: {str(ex)}") 
            return []
    
    def write_execel(self):
        if not self.validate():
            return
        return