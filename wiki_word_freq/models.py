"""
Data models for the Wikipedia Word-Frequency Dictionary API.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class WordFrequencyResponse(BaseModel):
    """Response model for word frequency data."""

    word_count: Dict[str, int] = Field(
        ..., description="Dictionary mapping words to their occurrence count"
    )
    word_frequency: Dict[str, float] = Field(
        ..., description="Dictionary mapping words to their frequency percentage"
    )


class KeywordsRequest(BaseModel):
    """Request model for the /keywords endpoint."""

    article: str = Field(
        ..., description="The title of the Wikipedia article to start from"
    )
    depth: int = Field(
        ..., description="The depth of traversal within Wikipedia articles", ge=0
    )
    ignore_list: Optional[List[str]] = Field(
        default=[], description="A list of words to ignore"
    )
    percentile: Optional[int] = Field(
        default=0,
        description="The percentile threshold for word frequency",
        ge=0,
        le=100,
    )
