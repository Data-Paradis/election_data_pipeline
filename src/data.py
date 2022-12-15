
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SourcesOfInterest:

    name: str
    affiliation: bool
    candidate: bool
    party: str
    role: str


@dataclass
class Content:
    
    date: datetime
    source: str
    content: str
    date_scraped: datetime
    link: str
