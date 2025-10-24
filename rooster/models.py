from dataclasses import dataclass
from typing import Optional

@dataclass
class JobResult:
    bucket: str
    title: str
    url: str
    snippet: Optional[str] = None

    def __str__(self):
        return f"[{self.bucket}] {self.title} → {self.url}"
