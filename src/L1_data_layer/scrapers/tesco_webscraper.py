from prefect import task, flow

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.L1_data_layer.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By


class TescoScraper(BaseScraper):
    def __init__(self, category: str, headless=True) -> None:
        super().__init__(headless)
        self.base_url = "https://www.tesco.com/groceries/en-GB/shop/"
        self.driver.get(self.base_url)
        self.category = category

    def set_category(self, category=None):
        if category is None:
            category = self.category
        category_url = f"{self.base_url}{category}/all?include-children=true"
        self.driver.get(category_url)

    def print_source(self):
        print("PRINTING SOURCE")
        print(self.driver.page_source)

    def process(self):
        self.set_category()
        # self.print_source()

        self.driver.get_screenshot_as_file("screenshot.png")

        product_title_xpath = "/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[6]/div/div/div[2]/div/ul/li[1]/div/div/div/div[1]/div[3]/h3/a/span"
        # product_title_xpath = "//*[@id='tile-300161315']/div[3]/h3/a/span"
        product_title_xpath = "/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[6]/div/div/div[2]/div/ul/li[2]/div/div/div/div[1]/div[3]/h3/a"

        price_xpath = "/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[6]/div/div/div[2]/div/ul/li[2]/div/div/div/div[1]/div[3]/div[2]/div[2]/div/div/form/div/div/div[1]/p[1]"
        price_xpath = '//*[@id="tile-293836686"]/div[3]/div[2]/div[2]/div/div/form/div/div/div[1]/p[1]'

        product_title = self.driver.find_elements(By.XPATH, product_title_xpath)
        price_obj = self.driver.find_elements(By.XPATH, price_xpath)

        print([x for x in product_title])
        print([x for x in price_obj])

        self.driver.get_screenshot_as_file("screenshot.png")

        self.quit()


if __name__ == "__main__":
    with TescoScraper(category="fresh-food") as scraper:
        scraper.process()
