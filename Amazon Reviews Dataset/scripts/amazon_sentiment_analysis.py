# Task 5: Perform Sentiment Analysis on Review Texts
import json
from mrjob.job import MRJob
from mrjob.step import MRStep
from textblob import TextBlob


class SentimentAnalysis(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.reducer_sort)
        ]

    def mapper(self, _, line):
        review = json.loads(line.strip())
        text = review['text']
        sentiment = TextBlob(text).sentiment.polarity
        if sentiment > 0:
            sentiment_category = 'positive'
        elif sentiment < 0:
            sentiment_category = 'negative'
        else:
            sentiment_category = 'neutral'
        # yield review['asin'], (1, sentiment_category)
        yield (review['asin'], review["product_category"]), (1, sentiment_category)

    def combiner(self, asin_category, values):
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        total_reviews = 0
        for count, sentiment in values:
            total_reviews += count
            sentiment_counts[sentiment] += 1
        yield asin_category, (total_reviews,  sentiment_counts)
    
    def reducer(self, asin_category, values):
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        total_reviews = 0
        for count, sentiment in values:
            total_reviews += count
            sentiment_counts[sentiment] += 1
        yield None, (total_reviews, asin_category, sentiment_counts)

    def reducer_sort(self, _, product_sentiments):
        sorted_products = sorted(product_sentiments, reverse=True, key=lambda x: x[0])
        for count, asin_category, sentiment_counts in sorted_products:
            yield asin_category, {'total_reviews': count, 'sentiment_counts': sentiment_counts}



if __name__ == '__main__':
    SentimentAnalysis.run()

