# Amazon Games Review Scraper & Rating Prediction

This project consists of two Python scripts designed to handle Amazon product reviews. The first script, AmazonReviewScraper.py, scrapes reviews from Amazon.com, while the second script, RatingPrediction.py, predicts ratings based on the collected reviews.

## 1. Amazon Games Review Scraper
### Description:
The AmazonReviewScraper.py script automates the process of gathering reviews from Amazon.com. It employs the Selenium WebDriver library to navigate through Amazon product pages, extract review details, and store them in a MongoDB database. The script collects information such as reviewer names, review ratings, review dates, review content, and more.

### Dependencies:
* Selenium: For automating web browser interactions.
* Pandas: For data manipulation and organization.
* MongoDB: For storing the scraped review data.
* Chrome WebDriver: Required for Selenium to control the Chrome browser.
* ChromeDriverManager: For automatic installation of Chrome WebDriver.

### Usage:
1. Ensure all dependencies are installed using pip (pip install -r requirements.txt).
2. Configure MongoDB connection parameters (host, port, database name, collection name) in the script.
3. Run the script (python AmazonReviewScraper.py) to start scraping reviews from Amazon.
4. The scraped review data will be stored in the specified MongoDB collection.

## 2. Rating Prediction from Reviews
### Description:
The RatingPrediction.py script focuses on predicting ratings based on the collected Amazon reviews. It preprocesses the text data by cleaning, tokenizing, removing stopwords, and lemmatizing the text. Then, it trains a Multinomial Naive Bayes classifier using the processed reviews and their corresponding ratings. Finally, the script predicts ratings for new reviews using the trained classifier.

### Dependencies:
* Pandas: For data manipulation and organization.
* NLTK (Natural Language Toolkit): For text preprocessing tasks.
* Scikit-learn: For machine learning tasks such as model training and prediction.
* MongoDB: For fetching training data from the previously scraped reviews.

### Usage:
1. Ensure all dependencies are installed using pip (pip install -r requirements.txt).
2. Configure MongoDB connection parameters (host, port, database name, collection name) in the script.
3. Run the script (python RatingPrediction.py) to preprocess data, train the classifier, and predict ratings for new reviews.
4. The script will output the predicted ratings for the new reviews.

## Additional Notes:
* Both scripts can be customized further to suit specific requirements or preferences.
* Ensure proper handling of sensitive information (such as MongoDB credentials) to maintain data security.
* For larger datasets or different types of reviews, consider adapting the preprocessing steps or using different machine-learning algorithms for better performance.

