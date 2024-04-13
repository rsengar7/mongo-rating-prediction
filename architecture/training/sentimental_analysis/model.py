import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import SENTIMENT_PREDICTION_MODEL_PATH, DB_HOST, DB_PORT, DB_NAME, DB_GAMES_REVIEW_COLLECTION, SENTIMENT_VECTORIZER_PATH
from database.db_operations import MongoDBConnection

# data = pd.read_csv("your_dataset.csv")
data = pd.read_csv("/Users/riteshsengar/Documents/GRA/RecommendationWeb/amazon_scrap/Amazon Reviews/amazon_reviews.csv")

# Initialize MongoDB connection
mongo_connection = MongoDBConnection(host=DB_HOST, port=DB_PORT, db_name=DB_NAME, collection_name=DB_GAMES_REVIEW_COLLECTION)

data_list = mongo_connection.fetch_data()

data = pd.DataFrame(data_list[:200000])


def sentiment_train(data):
    X_train, X_test, y_train, y_test = train_test_split(data['Review'], data['rating_label'], test_size=0.2, random_state=42)

    vectorizer = CountVectorizer()
    X_train_vectors = vectorizer.fit_transform(X_train)
    X_test_vectors = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vectors, y_train)

    # Save Vectorizer
    with open(SENTIMENT_VECTORIZER_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)

    # Save model
    with open(SENTIMENT_PREDICTION_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    y_pred = model.predict(X_test_vectors)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)



def review_sentiment_prediction(text):
    with open(SENTIMENT_VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)

    with open(SENTIMENT_PREDICTION_MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    # vectorizer = CountVectorizer()

    new_review_vector = vectorizer.transform([text])

    predicted_sentiment = model.predict(new_review_vector)

    if predicted_sentiment == 1:
        print("Positive sentiment")
    else:
        print("Negative sentiment")

# new_review_text = "This product is fantastic!"
# review_sentiment_prediction(new_review_text)
