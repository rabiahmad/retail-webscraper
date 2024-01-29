<<<<<<< HEAD
from prefect import task, flow

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.L1_data_layer.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
=======
import asyncio
from playwright.async_api import async_playwright
from src.L1_data_layer.scrapers.base_scraper import BaseScraper
import logging
>>>>>>> 24b4b3f (resolved conflicts)


class TescoScraper(BaseScraper):
    def __init__(self, category: str, headless=True) -> None:
        super().__init__(headless)
        self.base_url = "https://www.tesco.com/groceries/en-GB/shop/"
<<<<<<< HEAD
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
=======
        self.category = category

    async def set_category(self, category=None):
        if category is None:
            category = self.category
        category_url = f"{self.base_url}{category}/all?include-children=true"
        try:
            await self.driver.goto(category_url)
            logging.info(f"Successfully navigated to category URL: {category_url}")
        except Exception as e:
            logging.error(
                f"Failed to navigate to category URL: {category_url}. Error: {e}"
            )

    async def print_source(self):
        print("PRINTING SOURCE")
        print(await self.driver.content())

    async def process(self):
        async with self:
            await self.set_category()

            await self.driver.screenshot(path="screenshot.png")

            product_title_xpath = "/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[6]/div/div/div[2]/div/ul/li[1]/div/div/div/div[1]/div[3]/h3/a/span"
            product_title_xpath = "/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[6]/div/div/div[2]/div/ul/li[2]/div/div/div/div[1]/div[3]/h3/a"

            price_xpath = "/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[6]/div/div/div[2]/div/ul/li[2]/div/div/div/div[1]/div[3]/div[2]/div[2]/div/div/form/div/div/div[1]/p[1]"
            price_xpath = '//*[@id="tile-293836686"]/div[3]/div[2]/div[2]/div/div/form/div/div/div[1]/p[1]'

            product_titles = await self.driver.query_selector_all(product_title_xpath)
            prices = await self.driver.query_selector_all(price_xpath)

            product_titles_text = [await x.text_content() for x in product_titles]
            prices_text = [await x.text_content() for x in prices]

            print(product_titles_text)
            print(prices_text)

            await self.driver.screenshot(path="screenshot.png")


if __name__ == "__main__":
    scraper = TescoScraper(category="fresh-food")
    scraper.run()
>>>>>>> 24b4b3f (resolved conflicts)
