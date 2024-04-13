import pandas as pd
# from training.rating_prediction.model import training
from training.sentimental_analysis.model import sentiment_train, review_sentiment_prediction
from database.db_operations import MongoDBConnection
from config import DB_GAMES_REVIEW_COLLECTION, DB_HOST, DB_NAME, DB_PORT

# Initialize MongoDB connection
mongo_connection = MongoDBConnection(host=DB_HOST, port=DB_PORT, db_name=DB_NAME, collection_name=DB_GAMES_REVIEW_COLLECTION)

data_list = mongo_connection.fetch_data()

data = pd.DataFrame(data_list[:200000])

# vectorizer = sentiment_train(data)

new_review_text = "This product is fantastic!"
review_sentiment_prediction(new_review_text)