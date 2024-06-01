import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Function to load data from a text file into a DataFrame
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            asin_category = eval(parts[0])
            avg_rating = float(parts[1])
            data.append({
                'product_id': asin_category[0],
                'category': asin_category[1],
                'avg_rating': avg_rating
            })
    return pd.DataFrame(data)

# Load the average ratings data
root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(root, '..', 'outputs', 'amazon_product_average_rating_output.txt'))
ratings_df = load_data(file_path)

# Summary statistics of average ratings
ratings_summary = ratings_df.groupby('category')['avg_rating'].describe()

# Count of products per category
category_counts = ratings_df['category'].value_counts()

# Set up the matplotlib figure
plt.figure(figsize=(14, 8))

# Box plot of average ratings by category
sns.boxplot(x='category', y='avg_rating', data=ratings_df)
plt.xticks(rotation=45)
plt.tight_layout() 
plt.title('Distribution of Average Ratings by Category')
plt.xlabel('Category')
plt.ylabel('Average Rating')
plt.savefig('averge_ratings_by_category.png')
plt.close()

# Histogram of average ratings
plt.figure(figsize=(10, 6))
sns.histplot(ratings_df['avg_rating'], bins=50, kde=True)
plt.title('Distribution of Average Ratings')
plt.xlabel('Average Rating')
plt.ylabel('Frequency')
plt.yscale('log')  # Set y-axis scale to logarithmic
plt.savefig('average_rating_distribution.png')
plt.close()

# Bar plot of the count of products per category
plt.figure(figsize=(15, 10))
category_counts.plot(kind='bar')
plt.title('Number of Products by Category')
plt.xlabel('Category')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)
plt.tight_layout() 
plt.savefig('number_of_products_by_category.png')
plt.close()
