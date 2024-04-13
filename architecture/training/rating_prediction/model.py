try:
    import re
    import pickle
    import warnings
    import pandas as pd
    from nltk import pos_tag
    from nltk.corpus import stopwords, wordnet
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import RegexpTokenizer, word_tokenize
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import MultinomialNB
    # from sklearn.externals import joblib
    
    # from pymongo import MongoClient

    from utils.data_processing import PreProcessing
    from database.db_operations import MongoDBConnection
    

    from config import DB_HOST, DB_NAME, DB_PORT, DB_GAMES_REVIEW_COLLECTION, RATING_PREDICTION_MODEL_PATH

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print("All the Modules are Successfully Imported")
except Exception as e:
    print("Enable to import all the necessary Modules---", e)


class DataProcessor():
    """
    Class to process data using preprocessing steps and train a classifier.
    """
    def __init__(self, data):
        self.data = data
        self.preprocessor = PreProcessing()

    def preprocess_data(self):
        """
        Method to preprocess data using various preprocessing steps.
        """
        self.data.loc[:, 'Review'] = self.data['Review'].astype(str)
        self.data.loc[:, 'Review'] = self.data['Review'].apply(self.preprocessor.clean_text)
        self.data.loc[:, 'Review'] = self.data['Review'].apply(self.preprocessor.remove_punctuations)
        self.data.loc[:, 'Review'] = self.data['Review'].apply(self.preprocessor.remove_stopwords)
        self.data.loc[:, 'Review'] = self.data['Review'].apply(self.preprocessor.word_stemmer)
        self.data.loc[:, 'Review'] = self.data['Review'].apply(self.preprocessor.missing_values)
        self.data = self.data.dropna(subset=['Review'])

    def train_classifier(self):
        """
        Method to train a Multinomial Naive Bayes classifier to predict ratings.
        """
        # Define TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=1000)
        X_vec = vectorizer.fit_transform(self.data['Review'])

        # Train a Multinomial Naive Bayes classifier to predict ratings
        model = MultinomialNB()
        model.fit(X_vec, self.data['Rating'])
        return vectorizer, model


class TextProcessor():
    """
    Class to process text data and predict ratings for new reviews.
    """

    def __init__(self, vectorizer, model):
        self.vectorizer = vectorizer
        self.model = model

    def preprocess_text(self, text):
        """
        Method to preprocess text data for prediction.
        """
        text = text.lower()
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        text = ' '.join(tokens)
        return text

    def predict_rating(self, new_review):
        """
        Method to predict rating for a new review.
        """
        processed_new_review = self.preprocess_text(new_review)
        new_review_vec = self.vectorizer.transform([processed_new_review])
        predicted_rating = self.model.predict(new_review_vec)[0]
        return predicted_rating


def model_training():
    # Initialize MongoDB connection
    mongo_connection = MongoDBConnection(host=DB_HOST, port=DB_PORT, db_name=DB_NAME, collection_name=DB_GAMES_REVIEW_COLLECTION)

    # Fetch data from MongoDB
    data_list = mongo_connection.fetch_data()

    # Convert data to DataFrame
    df = pd.DataFrame(data_list)

    # Preprocess data
    data_processor = DataProcessor(df)
    data_processor.preprocess_data()

    # Train classifier
    vectorizer, model = data_processor.train_classifier()

    # Save model to a file
    # Save model
    with open(RATING_PREDICTION_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    # joblib.dump(model, RATING_PREDICTION_MODEL_PATH)

def training():
    # Initialize MongoDB connection
    mongo_connection = MongoDBConnection(host=DB_HOST, port=DB_PORT, db_name=DB_NAME, collection_name=DB_GAMES_REVIEW_COLLECTION)

    # Fetch data from MongoDB
    data_list = mongo_connection.fetch_data()

    # Convert data to DataFrame
    df = pd.DataFrame(data_list[:200000])

    # Preprocess data
    data_processor = DataProcessor(df.head(99000))
    data_processor.preprocess_data()

    # Train classifier
    vectorizer, model = data_processor.train_classifier()

    # Save model to a file
    # Save model
    with open(RATING_PREDICTION_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    # joblib.dump(model, RATING_PREDICTION_MODEL_PATH)

    # Initialize TextProcessor
    text_processor = TextProcessor(vectorizer, model)

    # Sample new reviews for prediction
    sample = df.tail(500)

    # Predict ratings for testing data
    predicted_ratings = []
    actual_ratings = []

    # Predict ratings for new reviews
    for review, rating in sample[['Review', 'Rating']].values.tolist():
        predicted_rating = text_processor.predict_rating(review)
        predicted_ratings.append(predicted_rating)
        actual_ratings.append(rating)
        print([review, rating])
        print("Predicted Rating for the new Review:", predicted_rating)
        print("*" * 100)


