from dataclasses import dataclass, field
from typing import List, Optional, Any
from core._enum import ActionKey, LocatorType

@dataclass
class Step:
    action: ActionKey
    locator: LocatorType = LocatorType.ID
    selector: Optional[str] = None
    value: Optional[Any] = None
    timeout: int = 3

    # { "action": "click",  "locator": "xpath", "selector": "//button[@id='submit']" }
    # { "action": "click",  "locator": "id",    "selector": "maso" }
    # { "action": "click",  "locator": "css",   "selector": "#maso" }
    # { "action": "click",  "locator": "name",  "selector": "maso" }
    # { "action": "click",  "locator": "class", "selector": "maso-input" }

    # { "action": "sleep",  "locator": "", "selector": "maso-input" }
    @classmethod
    def from_dict(cls, data: dict):
        action_key = ActionKey(data.get("action"))
        locator_key = LocatorType(data.get("locator", "id"))
        selector = data.get("selector")
        value = data.get("value")
        timeout = data.get("timeout", 3)

        if not selector:
            for ltr in LocatorType:
                if ltr.value in data:
                    selector = data.get(ltr.value)
                    locator = ltr
                    break 
        return cls(
            action = action_key,
            locator = locator,
            value = value,
            timeout = timeout
        )

       

class AutomationSteps:
    url: str
    steps: List[Step] =field(default_factory=list)