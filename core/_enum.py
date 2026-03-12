from enum import Enum

class ActionKey(Enum):
    FILL = "FILL"
    CLICK = "CLICK"
    SLEEP = "SLEEP"
    WAIT_VISIBLE = "WAIT_VISIBLE"

class LocatorType(Enum):
    ID = "id"
    TEXT = "text"
    XPATH = "xpath"
    CSS = "css"
    NAME = "name"
    CLASS = "class"
    
