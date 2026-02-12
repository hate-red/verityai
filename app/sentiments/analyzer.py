import re
import torch
import matplotlib.pyplot as plt

from razdel import sentenize
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.signal import savgol_filter


def preprocess_text(raw_text: str | bytes) -> list[str]:
    text = raw_text.replace('\n', ' ') # type: ignore
    cleaned_text = re.sub(r'\s+', ' ', text) # type: ignore
    sentences = [sent.text for sent in sentenize(cleaned_text)]

    return sentences


class SentimentAnalyzer:
    def __init__(self):
        self.__model_checkpoint = 'cointegrated/rubert-tiny-sentiment-balanced'
        self.__tokenizer = AutoTokenizer.from_pretrained(self.__model_checkpoint)
        self.__model = AutoModelForSequenceClassification.from_pretrained(self.__model_checkpoint)

        if torch.cuda.is_available():
            self.__model.cuda()


    def estimate_sentiment(self, raw_text: str | bytes) -> list[float]:
        """
        Core function that does sentiment analysis.
        It processes `raw_text` to a list of floats that 
        respresent sentiments: one sentence - one sentiment
        """

        sentences = preprocess_text(raw_text)
        sentiment_result = []

        for sentence in sentences:
            with torch.no_grad():
                inputs = self.__tokenizer(
                    sentence, return_tensors='pt', truncation=True, padding=True
                ).to(self.__model.device)
                proba = torch.sigmoid(self.__model(**inputs).logits).cpu().numpy()[0]

                sentiment_result.append(proba.dot([-1, 0, 1]))

        return sentiment_result



class GraphCreator:
    def __init__(self, data: list):
        self.data = data
        self.filtered_data = []
    

    def ensemble_filter(self, number_of_filters: int = 100):
        data_length = len(self.data)

        start = data_length // 10
        stop = data_length // 4
        step = (stop - start) // number_of_filters
        step = step if step != 0 else 1

        all_filters = 0

        for window_length in range(start, stop, step):
            filtered = savgol_filter(self.data, window_length=window_length, polyorder=0)
            all_filters += filtered
        
        self.filtered_data = all_filters / number_of_filters

        return type(self.filtered_data)


    def create_graph(self, show: bool = False, numer_of_filters = 100) -> None:
        self.ensemble_filter(numer_of_filters)

        plt.figure(figsize=(8, 6), dpi=100)
        plt.plot(self.filtered_data)
        plt.xlabel('Number of sentence')
        plt.ylabel('Sentiment')
        plt.grid()

        if show:
            plt.show()
