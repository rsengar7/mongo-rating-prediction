import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class AmazonReviewScraper:
    def __init__(self):
        # Setting up Chrome options
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu') 
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        # Initialize Chrome service
        self.service = Service(ChromeDriverManager().install())
        # Initialize WebDriver
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)


    def scrape_reviews(self):
        Names = []
        name_url = []
        user_id = []
        Review_rating = []
        Review_date = []
        Review = []
        ASIN = []
        star_rating = []
        review_location = []

        # Loop through product pages
        for i in range(1, 331):
            product_url = f"https://www.amazon.com/s?i=mobile-apps&rh=n%3A9209902011&fs=true&page={i}&qid=1710971883&ref=sr_pg_2"
            self.driver.get(product_url)
            time.sleep(2)

            # Loop through each product
            for j in range(1, 62):
                try:
                    xpath = f"/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{j}]/div/div/span/div/div/div[1]/span/a"
                    data = self.driver.find_element(by=By.XPATH, value=xpath)
                    baseurl = data.get_attribute('href')
                    base_url = baseurl.split("/ref")[0].replace('dp', 'product-reviews')
                    all_review_part = "/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar={}&pageNumber={}"
                    
                    # Loop through star ratings
                    for number, star in {1: 'one_star', 2: 'two_star', 3: 'three_star', 4: 'four_star', 5: 'five_star'}.items():
                        review_url = base_url + all_review_part
                        page_num = 11

                        try:
                            url1 = review_url.format(star, 1)
                            self.driver.get(url1)
                            time.sleep(1)

                            # Extract total reviews and calculate page numbers
                            total_reviews = self.driver.find_element(by=By.CSS_SELECTOR, value="div[data-hook='total-review-count']").text
                            total_reviews = int(total_reviews.replace(",", ""))
                            page_num = min(11, (total_reviews // 10) + 1)

                            # Loop through review pages
                            for page in range(1, page_num):
                                url = review_url.format(star, page)
                                self.driver.get(url)
                                time.sleep(1)

                                # Extract review details
                                review_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value="div[data-hook='review']")
                                for element in review_elements:
                                    try:
                                        Names.append(element.find_element(by=By.CSS_SELECTOR, value="span.a-profile-name").text)
                                    except:
                                        Names.append("")

                                    try:
                                        rating_element = element.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']")
                                        Review_rating.append(rating_element.text)
                                    except:
                                        Review_rating.append("")
                                    
                                    try:
                                        date_element = element.find_element(by=By.CSS_SELECTOR, value="span[data-hook='review-date']")
                                        Review_date.append(date_element.text)
                                        review_location.append(date_element.text.split("on")[0].strip())
                                    except:
                                        Review_date.append("")
                                        review_location.append("")
                                    
                                    try:
                                        review_element = element.find_element(by=By.CSS_SELECTOR, value="span[data-hook='review-body']")
                                        Review.append(review_element.text)
                                    except:
                                        Review.append("")
                                    
                                    try:
                                        url_element = element.find_element(by=By.CSS_SELECTOR, value="a.a-profile")
                                        name_url.append(url_element.get_attribute("href"))
                                        user_id.append(url_element.get_attribute("href").split("account.")[1].split("/")[0])
                                        print("User Id : ",url_element.get_attribute("href").split("account.")[1].split("/")[0])
                                    except:
                                        name_url.append("")
                                        user_id.append("")
                                    
                                    ASIN.append(baseurl.split("/")[5])
                                    star_rating.append(number)
                        except:
                            pass
                except:
                    pass


        # Construct DataFrame from scraped data
        data_dict = {
            "ASIN": ASIN,
            "User_id": user_id,
            "Names": Names,
            "Review_rating": Review_rating,
            "Review_date": Review_date,
            "Rating": star_rating,
            "Review Location": review_location,
            "Review": Review,
            "User_url": name_url
        }

        df = pd.DataFrame(data_dict)
        return df


    def save_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename, index=False)


    def close_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = AmazonReviewScraper()
    scraped_data = scraper.scrape_reviews()
    scraper.save_to_csv(scraped_data, "amazon_reviews.csv")
    scraper.close_driver()
