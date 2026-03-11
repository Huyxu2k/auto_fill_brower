import json
import os
from loguru import logger
from typing import List, Optional, Any
from models.step import AutomationSteps, Step


class LoaderManager:
    def __init__(self, json_path: str):
        # check path, check định dạng file
        self.json_path = json_path

    def load_config(self) -> Optional[AutomationSteps]:
        # Map đối tượng từ joson sang Step và add vào AutomationSteps
        # TODO
        return
