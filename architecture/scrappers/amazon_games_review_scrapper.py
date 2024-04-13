try:
    # Import necessary libraries
    import time
    import json
    import warnings
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from pymongo import MongoClient
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # Ignore deprecation warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Notify successful import of modules
    print("All the Modules are Successfully Imported")
except Exception as e:
    # Notify if any error occurs during module import
    print("Enable to import all the necessary Modules---", e)


class MongoDBConnection():
    """
    Class to establish a connection to MongoDB and fetch data.
    """
    def __init__(self, host='localhost', port=27017, db_name=None, collection_name=None):
        # Initialize MongoDB connection
        self.client = MongoClient(f'{host}:{port}')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_one(self, document):
        """
        Insert a single document into the collection.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def insert_many(self, documents):
        """
        Insert multiple documents into the collection.
        """
        result = self.collection.insert_many(documents)
        return result.inserted_ids
    

class AmazonReviewScraper:
    def __init__(self, mongo_connection):
        # Initialize Chrome webdriver and MongoDB connection
        self.mongo_connection = mongo_connection
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        # Set Chrome options for WebDriver
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu') 
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Initialize Chrome service and WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        return driver
    
    def sentiment_label(self, text):
        # Analyze sentiment of text using VADER SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(text)
        rating_label = "pos" if sentiment['compound'] > 0 else "neg"
        return rating_label


    def scrape_reviews(self, output_file):
        # Initialize lists to store scraped data
        Names = []
        name_url = []
        user_id = []
        Review_rating = []
        Review_date = []
        Review = []
        ASIN = []
        Star_rating = []
        Review_location = []
        Rating_label = []

        # Loop through product pages
        for i in range(1,331):
            product_url = "https://www.amazon.com/s?i=mobile-apps&rh=n%3A9209902011&fs=true&page={}&qid=1710971883&ref=sr_pg_2".format(i)
            self.driver.get(product_url)
            time.sleep(2)

            # Loop through each product
            for j in range(1, 62):
                try:
                    # Extract product URL
                    xpath = "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{}]/div/div/span/div/div/div[1]/span/a".format(j)
                    data = self.driver.find_element(by=By.XPATH, value=xpath)
                    baseurl = data.get_attribute('href')
                    base_url = self._extract_base_url(baseurl)

                    # Generate review URL for one star rating
                    review_url = base_url + self._get_review_url_suffix('one_star', 1)
                    rate = self._get_review_rate_details(review_url)

                    # Determine the rating for the product
                    if rate == 0:
                        stars = {1: 'one_star'}
                    else:
                        stars = self._get_star_ratings()

                    # Loop through each star rating
                    for number, star in stars.items():
                        review_url = base_url + self._get_review_url_suffix(star, 1)
                        page_num = 11
                        rate = self._get_review_rate_details(review_url)
                        review_number = self._get_review_number_details(review_url)

                        # Determine the number of pages for reviews
                        if rate == 0:
                            page_num = 1
                        elif review_number in list(range(0, 10)):
                            page_num = 2
                        elif review_number in list(range(10, 20)):
                            page_num = 3
                        elif review_number in list(range(20, 30)):
                            page_num = 4
                        elif rate in list(range(1, 10)):
                            page_num = 2
                        elif rate in list(range(10, 20)):
                            page_num = 3
                        elif rate in list(range(20, 30)):
                            page_num = 4
                        elif rate in list(range(30, 40)):
                            page_num = 5
                        elif rate in list(range(40, 50)):
                            page_num = 6
                        elif rate in list(range(50, 60)):
                            page_num = 7
                        elif rate in list(range(60, 70)):
                            page_num = 8
                        elif rate in list(range(70, 80)):
                            page_num = 9
                        else:
                            pass

                        # Loop through each page of reviews
                        for i in range(1, page_num):
                            url = base_url + self._get_review_url_suffix(star, i)
                            self.driver.get(url)
                            time.sleep(1)

                            # Loop through each review on the page
                            for j in range(1, 11):
                                try:
                                    # Extract reviewer's name
                                    user_name = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{}]/div/div/div[1]/a/div[2]/span".format(j)).text
                                except:
                                    user_name = ""

                                try:
                                    # Extract review rating
                                    review_rating = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{}]/div/div/div[2]/a".format(j)).text
                                except:
                                    review_rating = ""

                                try:
                                    # Extract user's profile link
                                    user_link = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{}]/div/div/div[1]/a".format(j)).get_attribute('href')
                                except:
                                    user_link = ""

                                try:
                                    # Extract review date
                                    review_date = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{}]/div/div/span".format(j)).text.split("on")[1].strip()
                                except:
                                    review_date = ""

                                try:
                                    # Extract review location
                                    review_location = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{}]/div/div/span".format(j)).text.split("on")[0].strip().split("the")[1].strip()
                                except:
                                    review_location = ""

                                try:
                                    # Extract review text
                                    review_text = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{}]/div/div/div[4]/span".format(j)).text
                                except:
                                    review_text = ""

                                # Append values to respective lists
                                if isinstance(review_text, str) and review_text != "":
                                    Names.append(user_name)
                                    Review_rating.append(review_rating)
                                    name_url.append(user_link)
                                    user_id.append(self._extract_user_id(user_link))
                                    Review_date.append(review_date)
                                    Review_location.append(review_location)
                                    Review.append(review_text)
                                    Rating_label.append(self.sentiment_label(review_text))
                                    ASIN.append(url.split("/")[5])
                                    Star_rating.append(number)

                                    # Create dictionary for review data
                                    review_json = {}
                                    review_json['Reviewer Id'] = self._extract_user_id(user_link)
                                    review_json['Reviewer Name'] = user_name
                                    review_json['Review_rating'] = review_rating
                                    review_json['Review_date'] = review_date
                                    review_json['Review Location'] = review_location
                                    review_json['Review'] = review_text
                                    review_json['review_label'] = self.sentiment_label(review_text)
                                    review_json['ASIN'] = url.split("/")[5]
                                    review_json['Rating'] = number

                                    # Insert review data into MongoDB
                                    try:
                                        self.mongo_connection.insert_one(review_json)
                                    except Exception as ex:
                                        print(ex)

                except Exception as ex:
                    pass

        # Create DataFrame and save to CSV
        df = pd.DataFrame({
            "ASIN": ASIN,
            "User_id": user_id,
            "Names": Names,
            "Review_rating": Review_rating,
            "Review_date": Review_date,
            "Rating": Star_rating,
            "Review Location": Review_location,
            "Review": Review,
            "Rating_label": Rating_label,
            "User_url": name_url
        })
        df.dropna(subset=['Review'], inplace=True)  # Drop rows with missing reviews
        df.to_csv(output_file, index=False)


    def _extract_base_url(self, url):
        # Extract base URL from product URL
        return url.split("/ref")[0].replace('dp', 'product-reviews')


    def _get_star_ratings(self):
        # Define star ratings mapping
        return {1: 'one_star', 2: 'two_star', 3: 'three_star', 4: 'four_star', 5: 'five_star'}


    def _get_review_url_suffix(self, star, num):
        # Generate review URL suffix based on star rating and page number
        return "/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar={}&pageNumber={}".format(star, num)


    def _get_review_number_details(self, url):
        # Extract total number of reviews
        self.driver.get(url)
        review_number = 6
        try:
            review_number_xpath = "/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]"
            data = self.driver.find_element(by=By.XPATH, value=review_number_xpath)
            print("Review Number : ",data.text)
            review_number = int(data.text.split(",")[1].strip().split(" ")[0])
        except:
            pass
        
        return review_number
    
    
    def _get_review_rate_details(self, url):
        # Extract total number of ratings
        self.driver.get(url)
        rate = 0
        try:
            total_xpath = "/html/body/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div[3]/span"
            rate = int(self.driver.find_element(by=By.XPATH, value=total_xpath).text.split(" ")[0].replace(",",""))
        except:
            pass

        return rate


    def _extract_user_id(self, user_link):
        # Extract user ID from user profile link
        try:
            return user_link.split("account.")[1].split("/")[0]
        except IndexError:
            return ""


if __name__ == "__main__":
    # Initialize MongoDB connection and scraper object
    mongo_connection = MongoDBConnection(host='localhost', port=27017, db_name='unstructured_project', collection_name='test_info')
    scraper = AmazonReviewScraper(mongo_connection)
    
    scraper.scrape_reviews("amazon_reviews.csv")
