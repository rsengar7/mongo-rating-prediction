import os
import sys
import urllib.request
import time
import re
import time
import json
import pandas as pd

from pymongo import MongoClient


client = MongoClient('localhost:27017')
db = client.unstructured_project
collection = db.product_info


df = pd.read_csv("/Users/riteshsengar/Documents/GRA/RecommendationWeb/amazon_scrap/Amazon Product Info/amazon_games_info.csv")
print(df.head())

print(df.columns)

cols = ['ASIN', 'Names', 'total_reviews', 'overall_rating',
       'game_price', 'game_size', 'developed_by', 'developer_email',
       'release_year', 'amazon_listed_date', 'language_supported', 'Ai_Review',
       'Ai_tags', 'product_description', 'product_features',
       'minimum_operating', 'application_permission', 'reviews_url']

df = df[cols]


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