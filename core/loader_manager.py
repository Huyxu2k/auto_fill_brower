import json
import os
from loguru import logger
from typing import List, Optional, Any
from models.step import AutomationSteps, Step


class LoaderManager:
    def __init__(self, json_path: str):
        self.json_path = json_path

    def load_config(self) -> Optional[AutomationSteps]:
        try:
            # check path, check định dạng file

            # Map đối tượng từ joson sang Step và add vào AutomationSteps
            # TODO
            return
        except FileNotFoundError:
            logger.error("Không tìm thấy file {self.json_path}")
            return None
        except json.JSONDecodeError:
            logger.error("File không đúng định dạng")
            return None
