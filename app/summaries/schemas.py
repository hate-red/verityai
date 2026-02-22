from pydantic import BaseModel


class SummaryPublic(BaseModel):
    """
    Response schema
    """
    id: int | None = None
    user_id: int | None = None
    source_text: str
    summarized_text: str


class SummaryPost(BaseModel):
    """
    Defines POST request schema
    """
    user_id: int | None = None
    source_text: str


class SummaryUpdate(BaseModel):
    """
    Schema for updating existing summary (e.g. regeneration) 
    """
    id: int
    updated_text: str


class SummaryDelete(BaseModel):
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
