from dataclasses import dataclass
from typing import List 


@dataclass
class ResumeProfile:
    name : str
    skills : List[str]
    experience_years : int
    roles : List[str]
