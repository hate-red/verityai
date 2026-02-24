from pydantic import BaseModel


class SentimentPublic(BaseModel):
    """
    Defines response schema for all sentiment endpoints
    """
    id: int | None = None
    user_id: int | None = None
    source_text: str
    sentiments: list[float]


class SentimentPost(BaseModel):
    """
    Defines POST request schema
    """
    source_text: str


class SentimentUpdate(BaseModel):
    """
    Schema for updating existing analysis
    source text here is an updated text that we want to reanalyze
    """
    id: int
    updated_text: str


class SentimentDelete(BaseModel):
    """
    Defines DELETE request schema 
    """ 
    id: int
