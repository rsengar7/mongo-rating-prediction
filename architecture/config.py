# config.py

# Database Connection
DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "unstructured_project"
DB_GAMES_REVIEW_COLLECTION = "product_reviews"
DB_GAMES_INFO_COLLECTION = "product_info"

# Models
RATING_PREDICTION_MODEL_PATH = "models/rating_prediction_model.pkl"
SENTIMENT_PREDICTION_MODEL_PATH = "models/sentiment_prediction_model.pkl"
SENTIMENT_VECTORIZER_PATH = "models/sentiment_vectorizer.pkl"

# Logging
LOG_LEVEL = "DEBUG"
LOG_FILE = "project.log"

# Dev Level
ENVIRONMENT = "development"

AMAZON_GAME_BASEURL = "https://www.amazon.com/s?i=mobile-apps&rh=n%3A9209902011&fs=true&page={}&qid=1710971883&ref=sr_pg_2"

# Scrapping Xpath
AMAZON_INFO_XPATH = {
    "games_name": "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/h1/span/span/span/span[2]",
    "ai_review": "/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/p[1]",
    "games_price": "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/span[2]/strong",
    "language_support": "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/span[2]",
    "tags": "/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div",
    "rating": "/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[1]/span[1]/div/div/div/div/div/div[2]/div/div[2]/div/span",
    "game_size": "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/div[1]/span[2]",
    "operating_system":  "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/div[5]/span[2]",
    "application_permission": "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/ul",
    "developer_name": "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/span/a",
    "developer_email": "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[{}]",
}

AMAZON_REVIEW_XPATH = "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{}]/div/div/span/div/div/div[1]/span/a"

AMAZON_REVIEW_CSS_SELECTOR = {
    "review_count": "div[data-hook='total-review-count']",
    "review_detail": "div[data-hook='review']",
    "reviewer_name": "span.a-profile-name",
    "short_review": "i[data-hook='review-star-rating']",
    "review_date_location": "span[data-hook='review-date']",
    "review": "span[data-hook='review-body']",
    "reviewer_info": "a.a-profile"
}