from dataclasses import dataclass, field
from typing import List, Optional, Any
from core._enum import ActionKey, LocatorType

class Step:
    id: int
    action: ActionKey
    locator: LocatorType = LocatorType.ID
    selector: Optional[str] = None
    value: Optional[Any] = None
    timeout: int = 3
    description: str =""

class AutomationSteps:
    url: str
    steps: List[Step] =field(default_factory=list)