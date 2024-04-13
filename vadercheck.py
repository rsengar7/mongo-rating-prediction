from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_label(text):
    analyzer = SentimentIntensityAnalyzer()

    sentiment = analyzer.polarity_scores(text)

    rating_label = "pos" if sentiment['compound'] > 0 else "neg"
    return rating_label

sentiment_label("worset case ever")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from joblib import dump, load


# data = pd.read_csv("your_dataset.csv")
data = pd.read_csv("/Users/riteshsengar/Documents/GRA/RecommendationWeb/amazon_scrap/Amazon Reviews/amazon_reviews.csv")

class NaiveBayes(object):
    def __init__(self):
        self.naive_obj = MultinomialNB()

    def training(self, tfidf_vect, tclass):
        self.train = self.naive_obj.fit(tfidf_vect, tclass)

    def testing(self, tfidf_vect):
        test = self.train.predict(tfidf_vect)
        return test


def sentiment_train(data):
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

    vectorizer = CountVectorizer()
    X_train_vectors = vectorizer.fit_transform(X_train)
    X_test_vectors = vectorizer.transform(X_test)

    nb = MultinomialNB()
    nb.fit(X_train_vectors, y_train)

    dump(nb, 'sentiment_model.joblib')

    y_pred = nb.predict(X_test_vectors)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

sentiment_train(data)

def review_sentiment_prediction(text):
    nb = load('sentiment_model.joblib')

    vectorizer = CountVectorizer()

    new_review_vector = vectorizer.transform([text])

    predicted_sentiment = nb.predict(new_review_vector)

    if predicted_sentiment == 1:
        print("Positive sentiment")
    else:
        print("Negative sentiment")

new_review_text = "This product is fantastic!"
review_sentiment_prediction(new_review_text)