from app.data_access import BaseDA
from app.sentiments.models import Sentiment

def format_instance(instance):
    instance.sentiments = [float(x) for x in instance.sentiments.split()]
    
    return instance


class SentimentDA(BaseDA): # type: ignore
    model = Sentiment

