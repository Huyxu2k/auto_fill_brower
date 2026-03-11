from enum import Enum

class ActionKey(Enum):
    FILL = "FILL"
    CLICK = "CLICK"
    SLEEP = "SLEEP"
    WAIT_VISIBLE = "WAIT_VISIBLE"

class LocatorType(Enum):
    ID = "ID"
    TEXT = "TEXT"
    XPATH = "XPATH"
    CSS = "CSS"
    NAME = "NAME"
    CLASS = "CLASS"
    
