import os
import sys
import urllib.request
import time
import re
import time
import json
import pandas as pd

from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


client = MongoClient('localhost:27017')
db = client.unstructured_project
collection = db.product_reviews


def sentiment_label(text):
    analyzer = SentimentIntensityAnalyzer()
    print(text)

    sentiment = analyzer.polarity_scores(text)

    rating_label = "pos" if sentiment['compound'] > 0 else "neg"
    print(rating_label, text)
    print("*"*100)
    return rating_label


df = pd.read_csv("/Users/riteshsengar/Documents/GRA/RecommendationWeb/amazon_scrap/Amazon Reviews/amazon_reviews.csv")
cols = ['ASIN', 'Reviewer Name', 'Review_rating', 'Review_date',
       'Rating', 'Review Location', 'Review']

df = df[cols]
df = df.dropna()
df['rating_label'] = df['Review'].apply(sentiment_label)
print(df.head())
print(df.columns)
# sys.exit()


# Convert DataFrame to JSON
json_data = df.to_json(orient='records')

parsed_json = json.loads(json_data)

# Pick the first JSON object
first_json_object = parsed_json[0]

# Print the first JSON object
# print(first_json_object)

for row in parsed_json:
    # print(row)
    # Insert one document into the collection
    insert_result = collection.insert_one(row)

    # Print the inserted document's ID
    print("Inserted document ID:", insert_result.inserted_id)

# Close the connection
client.close()