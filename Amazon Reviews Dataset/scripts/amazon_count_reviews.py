# Task 1.3.2: Count the number of reviews for each product
from mrjob.job import MRJob
from mrjob.step import MRStep
import json


class ReviewCount(MRJob):
    def mapper(self, _, line):
        review = json.loads(line.strip())
        # yield review['asin'], 1
        yield (review['asin'], review["product_category"]), 1

    def combiner(self, asin_category, counts):
        total_count = sum(count for count in counts)
        yield asin_category, total_count
    
    def reducer(self, asin_category, counts):
        total_count = sum(count for count in counts)
        yield asin_category, total_count

if __name__ == '__main__':
    ReviewCount.run()
