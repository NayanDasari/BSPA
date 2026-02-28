from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime

@dataclass
class Indicator:
    """
    Represents a specific stress indicator or behavioral factor.
    """
    name: str
    value: float  # 0.0 to 1.0 (normalized) for Likert, or -1 for text-only
    description: str
    domain: str
    variability: float = 0.0  # Measure of fluctuation over time if available
    trend: str = "Stable"  # "Improving", "Worsening", "Stable"
    text_value: str = ""  # For open-ended responses

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "description": self.description,
            "domain": self.domain,
            "variability": self.variability,
            "trend": self.trend,
            "text_value": self.text_value
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Indicator':
        return Indicator(**data)

@dataclass
class Domain:
    """
    Represents a broader category of mental health factors (e.g., Biological, Psychological).
    """
    name: str
    indicators: List[Indicator] = field(default_factory=list)

    def add_indicator(self, indicator: Indicator):
        self.indicators.append(indicator)

    @property
    def average_level(self) -> float:
        numeric_inds = [ind for ind in self.indicators if ind.value >= 0]
        if not numeric_inds:
            return 0.0
        return sum(ind.value for ind in numeric_inds) / len(numeric_inds)

    @property
    def max_variability(self) -> float:
        if not self.indicators:
            return 0.0
        return max(ind.variability for ind in self.indicators)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "indicators": [ind.to_dict() for ind in self.indicators]
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Domain':
        domain = Domain(name=data["name"])
        domain.indicators = [Indicator.from_dict(ind_data) for ind_data in data.get("indicators", [])]
        return domain

@dataclass
class Pattern:
    """
    Represents a detected pattern or interaction effect.
    """
    name: str
    description: str
    severity: str  # "Low", "Moderate", "Elevated" - descriptive, not diagnostic
    involved_domains: List[str]
    evidence_context: str  # Creating a link to research
    protective_factors: List[str] = field(default_factory=list)
    confidence: str = "Moderate" # "High", "Moderate", "Tentative"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
            "involved_domains": self.involved_domains,
            "evidence_context": self.evidence_context,
            "protective_factors": self.protective_factors,
            "confidence": self.confidence
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Pattern':
        return Pattern(**data)

@dataclass
class UserSession:
    """
    Holds the state for a single assessment session.
    """
    timestamp: datetime = field(default_factory=datetime.now)
    domains: Dict[str, Domain] = field(default_factory=dict)
    identified_patterns: List[Pattern] = field(default_factory=list)
    data_completeness: float = 0.0 # 0.0 to 1.0

    def add_domain(self, domain: Domain):
        self.domains[domain.name] = domain

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "domains": {k: v.to_dict() for k, v in self.domains.items()},
            "identified_patterns": [p.to_dict() for p in self.identified_patterns],
            "data_completeness": self.data_completeness
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UserSession':
        # Default fallback for completeness if missing from old data
        completeness = data.get("data_completeness", 0.0)
        
        session = UserSession(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            data_completeness=completeness
        )
        session.domains = {k: Domain.from_dict(v) for k, v in data.get("domains", {}).items()}
        session.identified_patterns = [Pattern.from_dict(p) for p in data.get("identified_patterns", [])]
        return session
