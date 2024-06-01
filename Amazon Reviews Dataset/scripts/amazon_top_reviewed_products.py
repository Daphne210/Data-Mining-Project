# Task 3: Find the Top Ten Most Reviewed Products
from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import sys


class TopTenReviewedProducts(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.top_ten_reducer)
        ]

    def mapper(self, _, line):
        review = json.loads(line.strip())
        # yield review['asin']), 1
        yield (review['asin'], review["product_category"]), 1

    def combiner(self, asin_category, counts):
        # Sum the counts for each ASIN-category pair
        total_count = sum(count for count in counts)
        yield asin_category, total_count
    
    def reducer(self, asin_category, counts):
        # Sum the counts for each ASIN-category pair
        total_count = sum(count for count in counts)
        yield None, (asin_category, total_count)

    def top_ten_reducer(self, _, product_counts):
        sorted_products = sorted(product_counts, reverse=True, key=lambda x: x[1])[:10]
        for asin_category, count in sorted_products:
            yield asin_category, count

if __name__ == '__main__':
    TopTenReviewedProducts.run()
