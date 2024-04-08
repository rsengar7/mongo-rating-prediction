import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class AmazonScraper:
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
        
    def scrape(self):
        ASIN = []
        Names = []
        Ai_Review = []
        Ai_tags = []
        overall_rating = []
        game_price = []
        language_supported = []
        release_year = []
        amazon_listed_date = []
        developed_by = []
        total_reviews = []
        product_description = []
        developer_email = []
        product_features = []
        minimum_operating = []
        game_size = []
        application_permission = []
        Review_contain_url = []

        for i in range(1, 331):
            product_url = "https://www.amazon.com/s?i=mobile-apps&rh=n%3A9209902011&fs=true&page={}&qid=1710971883&ref=sr_pg_2".format(i)

            self.driver.get(product_url)
            time.sleep(2)

            for j in range(1, 62):
                try:            
                    xpath = "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{}]/div/div/span/div/div/div[1]/span/a".format(j)

                    data = self.driver.find_element(by=By.XPATH, value=xpath)

                    url = data.get_attribute('href')

                    try:
                        base_url = url.split("/ref")[0].replace('dp', 'product-reviews')
                        all_review_part = "/ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"

                        review_url = base_url + all_review_part

                        self.driver.get(url)

                        time.sleep(1)
                        ASIN.append(url.split("/")[5])
                        Review_contain_url.append(review_url)
                        try:
                            name_xpath = "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/h1/span/span/span/span[2]"
                            data = self.driver.find_element(by=By.XPATH, value=name_xpath)
                            Names.append(data.text)
                        except:
                            Names.append("")

                        try:
                            ai_review_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/p[1]"
                            data = self.driver.find_element(by=By.XPATH, value=ai_review_xpath)
                            Ai_Review.append(data.text)
                        except:
                            Ai_Review.append("")

                        try:
                            price_xpath = "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/span[2]/strong"
                            data = self.driver.find_element(by=By.XPATH, value=price_xpath)
                            game_price.append(data.text)
                        except:
                            game_price.append("")

                        try:
                            lan_support_xpath = "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/span[2]"
                            data = self.driver.find_element(by=By.XPATH, value=lan_support_xpath)
                            language_supported.append(data.text)
                        except:
                            language_supported.append("")

                        try:
                            tag_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div"
                            data = self.driver.find_element(by=By.XPATH, value=tag_xpath)
                            Ai_tags.append(", ".join(data.text.split("\n")))
                        except:
                            Ai_tags.append("")

                        try:
                            overall_rating_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[1]/span[1]/div/div/div/div/div/div[2]/div/div[2]/div/span"
                            data = self.driver.find_element(by=By.XPATH, value=overall_rating_xpath)
                            overall_rating.append(data.text.split(" ")[0])
                        except:
                            overall_rating.append("")

                        try:
                            game_size_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/div[1]/span[2]"
                            data = self.driver.find_element(by=By.XPATH, value=game_size_xpath)
                            game_size.append(data.text.split(" ")[0])
                        except:
                            game_size.append("")

                        try:
                            minimum_operating_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/div[5]/span[2]"
                            data = self.driver.find_element(by=By.XPATH, value=minimum_operating_xpath)
                            minimum_operating.append(data.text.split(" ")[0])
                        except:
                            minimum_operating.append("")

                        try:
                            application_permission_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/ul"
                            data = self.driver.find_element(by=By.XPATH, value=application_permission_xpath)
                            application_permission.append(data.text.split(" ")[0])
                        except:
                            application_permission.append("")

                        try:
                            developed_by_xpath = "/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/span/a"
                            data = self.driver.find_element(by=By.XPATH, value=developed_by_xpath)
                            developed_by.append(data.text.split(" ")[0])
                        except:
                            developed_by.append("")

                        release = ""
                        first_list = ""
                        creator = ""
                        review_count = ""
                        prod_desc = ""
                        dev_email = ""
                        prod_features = ""
                        for i in range(1, 15):
                            try:
                                developer_email_xpath = "/html/body/div[1]/div[1]/div/div[2]/div[2]/div[{}]".format(i)
                                data = self.driver.find_element(by=By.XPATH, value=developer_email_xpath)
                                entry = data.text
                                if "Release Date" in entry:
                                    release = entry.split(":")[1].strip()
                                elif "Date first listed on Amazon" in entry:
                                    first_list = entry.split(":")[1].strip()
                                elif "Customer reviews" in entry:
                                    review_count = entry.split("\n")[1].split(" ")[0]
                                elif "Product description" in entry:
                                    prod_desc = "\n".join(entry.split("\n")[1:])
                                elif "Developer info" in entry:
                                    dev_email = entry.split("\n")[1].strip()
                                elif "Product features" in entry:
                                    prod_features = "\n".join(entry.split("\n")[1:])  
                            except:
                                pass

                        if release != "":
                            release_year.append(release)
                        else:
                            release_year.append("")

                        if first_list != "":
                            amazon_listed_date.append(first_list)
                        else:
                            amazon_listed_date.append("")

                        if review_count != "":
                            total_reviews.append(review_count)
                        else:
                            total_reviews.append("")

                        if prod_desc != "":
                            product_description.append(prod_desc)
                        else:
                            product_description.append("")

                        if dev_email != "":
                            developer_email.append(dev_email)
                        else:
                            developer_email.append("")

                        if prod_features != "":
                            product_features.append(prod_features)
                        else:
                            product_features.append("")

                    except:
                        pass

                except:
                    pass

        # Construct DataFrame from scraped data
        data_dict = {
          "ASIN": ASIN,
          "Names": Names, 
          "total_reviews": total_reviews,
          "overall_rating": overall_rating, 
          "game_price": game_price, 
          "game_size": game_size, 
          "developed_by": developed_by, 
          "developer_email": developer_email, 
          "release_year": release_year, 
          "amazon_listed_date": amazon_listed_date, 
          "language_supported": language_supported, 
          "Ai_Review": Ai_Review, 
          "Ai_tags": Ai_tags, 
          "product_description": product_description, 
          "product_features": product_features, 
          "minimum_operating": minimum_operating, 
          "application_permission": application_permission,
          "reviews_url": Review_contain_url
        }

        df = pd.DataFrame(data_dict)

        return df

    def save_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename, index=False)

    def close_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = AmazonScraper()
    scraped_data = scraper.scrape()
    scraper.save_to_csv(scraped_data, "amazon_games_info.csv")
    scraper.close_driver()
