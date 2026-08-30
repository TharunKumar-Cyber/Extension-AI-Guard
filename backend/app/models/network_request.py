from datetime import datetime

from pydantic import BaseModel, Field


class NetworkRequest(BaseModel):
    """Represent a network request observed by Extension AI Guard."""

    request_id: str = Field(
        ...,
        description="Unique identifier for the network request",
    )
    url: str = Field(
        ...,
        description="Requested URL",
    )
    method: str = Field(
    ...,
    pattern="^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)$",
    description="HTTP method used by the request",
)
    domain: str = Field(
        ...,
        description="Destination domain",
    )
    timestamp: datetime = Field(
        ...,
        description="Time when the request was observed",
    )