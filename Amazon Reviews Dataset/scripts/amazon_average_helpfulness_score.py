# # Task 4: Calculate the Average Helpfulness Score for Reviews
from mrjob.job import MRJob
from mrjob.step import MRStep
import json


class AverageHelpfulnessScore(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer),
            MRStep(reducer=self.reducer_sort)
        ]

    def mapper(self, _, line):
        review = json.loads(line.strip())
        # yield review['asin'], review['helpful_vote']
        yield (review['asin'], review["product_category"]), review['helpful_vote']

    def combiner(self, asin_category, votes):
        total_scores = 0
        num_scores = 0
        for vote in votes:
            total_scores += vote
            num_scores += 1
        yield asin_category, (total_scores, num_scores)

    def reducer(self, asin_category, votes):
        total_scores = 0
        num_scores = 0
        for total, count in votes:
            total_scores += total
            num_scores += count    
        yield None, (asin_category, total_scores / num_scores)

    def reducer_sort(self, _, helpfulness_scores):
        sorted_products = sorted(helpfulness_scores, reverse=True, key=lambda x: x[1])
        for asin_category, score in sorted_products:
            yield asin_category, score


if __name__ == '__main__':
    AverageHelpfulnessScore.run()
