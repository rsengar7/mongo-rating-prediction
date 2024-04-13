import re
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer, word_tokenize

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