"""
Shared Pydantic models for HAL Guardian.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class Finding(BaseModel):
    severity: str
    category: str
    line: Optional[str] = ""
    description: str
    recommendation: str


class CodeReviewResult(BaseModel):
    file_path: str
    language: str
    model: str
    execution_status: str
    summary_table: dict
    findings: List[Finding]
    verdict: str
    rationale: str
    raw_response: str = ""


class DecodedPayload(BaseModel):
    type: str
    encoded: str
    decoded: str


class TrustReport(BaseModel):
    model_config = ConfigDict(extra="allow")

    source: str
    trust_level: str
    contains_command_language: bool
    contains_meta_instruction: bool
    contains_encoded_payload: bool
    decoded_payloads: List[DecodedPayload]
    findings: List[str]
    recommendation: str
    sanitized_text: str
    deep_analysis: Optional[Dict[str, Any]] = None


class AuditEntry(BaseModel):
    timestamp: str
    instance_id: str = ""
    action_type: str
    target: str
    model: str = ""
    status: str
    success: bool
    output_summary: str
    metadata: dict


class HealthSnapshot(BaseModel):
    timestamp: str
    total_actions: int
    successful_actions: int
    failed_actions: int
    recent_failures: List[dict]
    ollama_status: str
    models_available: List[str]
