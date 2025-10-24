from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class JobResult:
    bucket: str
    title: str
    url: str
    snippet: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    tech_stack: List[str] = field(default_factory=list)
    description: Optional[str] = None

    def __str__(self):
        stack_str = ", ".join(self.tech_stack) if self.tech_stack else "-"
        return f"[{self.bucket}] {self.title} @ {self.company or '?'} ({self.location or '-'}) → {self.url} [{stack_str}]"
