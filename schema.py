from dataclasses import dataclass
from typing import *
from enum import Enum

from cborGenerationProject.recurseGuy.generator import *

#________EDIT HERE________

class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

@dataclass
class Wrapper:
    src: str
    dest: str
    prio: int
    weekday: Weekday
    m: Dict[str,int]
    f: float
    b: bool
    ttl: int

@dataclass
class MyClass:
    v: Wrapper
    w: Dict[str,List[float]]
    x: Annotated[List[int], 10]
    y: Dict[str,List[Dict[str,int]]]
    z: Dict[str,Dict[int,List[str]]]

generateCPP(Weekday, Wrapper, MyClass)
#________EDIT HERE________