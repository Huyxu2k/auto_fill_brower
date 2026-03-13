from enum import Enum

class ActionKey(Enum):
    FILL = "fill"
    CLICK = "click"
    SLEEP = "sleep"
    WAIT = "wait"

class LocatorType(Enum):
    ID = "id"
    TEXT = "text"
    XPATH = "xpath"
    CSS = "css"
    NAME = "name"
    CLASS = "class"
    
