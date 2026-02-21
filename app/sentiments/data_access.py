from app.data_access import BaseDA
from app.sentiments.models import Sentiment


class SentimentDA(BaseDA): # type: ignore
    model = Sentiment

