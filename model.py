try:
    import re
    import warnings
    import pandas as pd
    import numpy as np
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import MultinomialNB
    from nltk.corpus import stopwords, wordnet
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import RegexpTokenizer, word_tokenize
    from nltk import pos_tag
    from pymongo import MongoClient

    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print("All the Modules are Successfully Imported")
except Exception as e:
    print("Enable to import all the necessary Modules---", e)


class PreProcessing():
    """
    Class to preprocess text data.
    """

    def __init__(self):
        self.sub = re.sub
        self.stemmer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words('english'))

    def __str__(self):
        return self.__class__.__name__

    def clean_text(self, text):
        """
        Method to perform initial cleaning of text data.
        """
        if isinstance(text, str):
            text = text.lower()
            # Replace contractions with full words
            text = self.sub(r"can't", "cannot", text)
            text = self.sub(r"won't", "will not", text)
            # Additional replacements for contractions
            text = self.sub(r"want's", "wants", text)
            text = self.sub(r"when'd", "when did", text)
            # Further substitutions and replacements
            text = self.sub(r"\'s", " is", text)
            text = self.sub(r"\'d", " had", text)
            text = self.sub(r"n't", " not", text)
            # More substitutions for contractions
            text = self.sub(r"\'ve", " have", text)
            text = self.sub(r"\'ll", " will", text)
            text = self.sub(r"\'m", " am", text)
            text = self.sub(r"\'re", " are", text)
            text = self.sub(r"can’t", "cannot", text)
            text = self.sub(r"won’t", "will not", text)
            text = self.sub(r"want’s", "wants", text)
            text = self.sub(r"when’d", "when did", text)
            text = self.sub(r"\’s", " is", text)
            text = self.sub(r"\’d", " had", text)
            text = self.sub(r"n’t", " not", text)
            text = self.sub(r"\’ve", " have", text)
            text = self.sub(r"\’ll", " will", text)
            text = self.sub(r"\’m", " am", text)
            text = self.sub(r"\’re", " are", text)
            # Replace other characters
            text = text.replace(":", " ")
            text = text.replace("?", "")
            # Remove numbers
            text = re.sub(r'\d+', '', text)
            return text

    def remove_punctuations(self, text):
        """
        Method to remove punctuations from text data.
        """
        if isinstance(text, str):
            tokenizer = RegexpTokenizer('\\w+|\\$[\\d\\.]+|\\S+')
            return ' '.join(tokenizer.tokenize(self.sub('[^a-zA-Z0-9]', ' ', text)))
        else:
            return ""

    def remove_stopwords(self, text):
        """
        Method to remove stopwords from text data.
        """
        return " ".join(word for word in word_tokenize(text) if word not in self.stopwords)

    def get_part_of_speech_tags(self, token):
        """
        Method to determine the part of speech of a token.
        """
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        tag = pos_tag([token])[0][1][0].upper()

        return tag_dict.get(tag, wordnet.NOUN)

    def word_stemmer(self, text):
        """
        Method to perform lemmatization of words in text data.
        """
        if isinstance(text, str):
            return " ".join([self.stemmer.lemmatize(word, self.get_part_of_speech_tags(word)) for word in word_tokenize(text)])
        else:
            return ""

    def missing_values(self, reviews):
        """
        Method to handle missing values in text data.
        """
        if isinstance(reviews, str):
            return reviews if reviews != "" else ""
        else:
            return ""


class MongoDBConnection():
    """
    Class to establish a connection to MongoDB and fetch data.
    """

    def __init__(self, host='localhost', port=27017, db_name=None, collection_name=None):
        self.client = MongoClient(f'{host}:{port}')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_data(self, query={}):
        """
        Method to fetch data from MongoDB.
        """
        cursor = self.collection.find(query)
        data_list = list(cursor)
        return data_list


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
        self.data['Review'] = self.data['Review'].astype(str)
        self.data['Review'] = self.data['Review'].apply(self.preprocessor.clean_text)
        self.data['Review'] = self.data['Review'].apply(self.preprocessor.remove_punctuations)
        self.data['Review'] = self.data['Review'].apply(self.preprocessor.remove_stopwords)
        self.data['Review'] = self.data['Review'].apply(self.preprocessor.word_stemmer)
        self.data['Review'] = self.data['Review'].apply(self.preprocessor.missing_values)
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


if __name__ == "__main__":
    # Initialize MongoDB connection
    mongo_connection = MongoDBConnection(host='localhost', port=27017, db_name='unstructured_project', collection_name='product_reviews')

    # Fetch data from MongoDB
    data_list = mongo_connection.fetch_data()

    # Convert data to DataFrame
    df = pd.DataFrame(data_list[:200000])

    # Preprocess data
    data_processor = DataProcessor(df.head(99000))
    data_processor.preprocess_data()

    # Train classifier
    vectorizer, model = data_processor.train_classifier()

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


