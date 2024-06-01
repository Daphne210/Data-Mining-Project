# Task 2: Determine the Average Star Rating for Each Product
from mrjob.job import MRJob
from mrjob.step import MRStep
import json

class AverageStarRating(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer),
            MRStep(reducer=self.reducer_sort)
        ]

    def mapper(self, _, line):
        review = json.loads(line.strip())
        # yield review['asin'], review['rating']
        yield (review['asin'], review["product_category"]), review['rating']

    def combiner(self, asin_category, ratings):
        total_ratings = 0
        num_ratings = 0
        for rating in ratings:
            total_ratings += rating
            num_ratings += 1
        yield asin_category, (total_ratings, num_ratings)

    def reducer(self, asin_category, ratings):
        total_ratings = 0
        num_ratings = 0
        for total, count in ratings:
            total_ratings += total
            num_ratings += count
        yield None, (asin_category, total_ratings / num_ratings)

    def reducer_sort(self, _, product_average_rating):
        sorted_products = sorted(product_average_rating, reverse=True, key=lambda x: x[1])
        for asin_category, average_rating in sorted_products:
            yield asin_category, average_rating


if __name__ == '__main__':
    AverageStarRating.run()

