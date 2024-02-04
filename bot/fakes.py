from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

@dataclass
class Usage:
    user_id: str
    predict_time: float
    prediction_id: str

def fixed_response():
    return ["https://previews.123rf.com/images/alexwhite/alexwhite1412/alexwhite141203022/35188258-test-icon.jpg"]

@dataclass
class FakePrediction:
    id: str
    metrics: Optional[Dict[str, Any]]
    output: List[str] = field(default_factory=fixed_response)
