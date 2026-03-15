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
        action_str = data.get("action", "").lower()
        try:
            action_key = ActionKey(action_str)
        except ValueError:
            # Fallback action if invalid or missing (optional, maybe raise it instead depending on needs)
            action_key = ActionKey.CLICK 

        locator_str = data.get("locator", "id").lower()
        try:
            locator_key = LocatorType(locator_str)
        except ValueError:
            locator_key = LocatorType.ID # Tự động lấy ID nếu sai

        selector = data.get("selector")
        value = data.get("value")
        timeout = data.get("timeout", 3)

        # Xử lý trường hợp không truyền 'selector' thông qua key rõ ràng, mà truyền hẳn key là type, vd {"id": "my_id"}
        if not selector:
            for ltr in LocatorType:
                if ltr.value in data:
                    selector = data.get(ltr.value)
                    locator_key = ltr
                    break 
                    
        return cls(
            action=action_key,
            locator=locator_key,
            selector=selector,
            value=value,
            timeout=timeout
        )

@dataclass
class AutomationSteps:
    url: str
    steps: List[Step] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: dict):
        url = data.get("url", "")
        steps_data = data.get("steps", [])
        steps_list = [Step.from_dict(step) for step in steps_data if isinstance(step, dict)]
        return cls(url=url, steps=steps_list)