from pydantic import BaseModel, Field


class DetectionResult(BaseModel):
    """Represent the result of a security analysis."""

    result_id: str = Field(
        ...,
        description="Unique identifier for the detection result",
    )
    request_id: str = Field(
        ...,
        description="Identifier of the analyzed network request",
    )
    is_malicious: bool = Field(
        ...,
        description="Whether the analyzed request is considered malicious",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence score between 0 and 1",
    )
    threat_type: str = Field(
        ...,
        description="Detected threat category",
    )
    explanation: str = Field(
        ...,
        description="Explanation of the detection result",
    )