from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class EmailState:
    emails: List[Dict[str, Any]] = field(default_factory=list)

    current_email: Dict[str, Any] = field(default_factory=dict)

    history: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    processed_count: int = 0

    spam_count: int = 0

    high_priority_count: int = 0

    reports: List[Dict[str, Any]] = field(default_factory=list)
