from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

DataT = TypeVar("DataT")


class Response(BaseModel, Generic[DataT]):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
    )
    status: str = "Success"
    data: Optional[DataT]


class TravelRecommendation(BaseModel):
    country: str
    season: str
    recommendations: List[str]


class ErrorDetail(BaseModel):
    type: str
    message: Optional[str]
    suggestions: Optional[List[str]]


class Error(BaseModel):
    error: ErrorDetail
