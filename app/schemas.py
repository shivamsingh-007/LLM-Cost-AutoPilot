from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class CompletionRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CompletionResponse(BaseModel):
    output: str
    request_id: str
    model_id: str
    routed_model: str
    complexity_tier: str
    selected_reason: str
    cost_usd: float
    latency_ms: float
    quality_score: float
    escalation_flag: bool
    success: bool


class StatsResponse(BaseModel):
    total_requests: int
    routed_cost: float
    baseline_cost: float
    cost_reduction_pct: float
    avg_latency_ms: float
    avg_quality_score: float
    escalations: int


class RoutingRule(BaseModel):
    tier: str
    preferred_models: List[str]
    min_quality_tier: int
    max_cost_per_1m_input: Optional[float] = None
    max_cost_per_1m_output: Optional[float] = None


class RoutingConfigUpdate(BaseModel):
    routing_mode: Optional[str] = None
    complexity_threshold_simple: Optional[float] = None
    complexity_threshold_medium: Optional[float] = None
    min_quality_score: Optional[float] = None
    rules: Optional[List[RoutingRule]] = None
