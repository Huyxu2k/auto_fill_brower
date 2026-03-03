from dataclasses import dataclass

@dataclass
class Person:
    id: str
    name: str
    yob: str # year of birth
    state: bool 