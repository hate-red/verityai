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
    user_id: int | None = None
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
    id: int | None = None
    source_text: str | None = None


    def to_dict(self) -> dict:
        """
        Transforms model to a dict,
        gets rid of all fields with value None.
        This is important so that delete operation works correctly
        """
        _ = {'id': self.id, 'source_text': self.source_text}
        transformed_model = {key: value for key, value in _.items() if value is not None}

        return transformed_model
