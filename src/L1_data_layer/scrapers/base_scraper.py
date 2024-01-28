from prefect import task, flow
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from abc import abstractmethod

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

from zenrows import ZenRowsClient

import toml

import logging


class BaseScraper:
    def __init__(self, headless=True) -> None:
        DRIVER_PATH = "C:/Users/rabi_/Projects/retail-webscraper/chromedriver.exe"  # TODO this should not be hard coded here
        self.service = Service(executable_path=DRIVER_PATH)
        self.options = webdriver.ChromeOptions()
        # self.options = Options()

        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        self.options.add_argument(f"user-agent={user_agent}")

        self.driver = self.create_undetected_headless_driver(
            options=self.options, service=self.service
        )

        self.driver.set_script_timeout(30)

        # self.driver = self.zenrows_client()

    def create_undetected_headless_driver(self, options, service, browser="Chrome"):
        if browser == "Chrome":
            if options is None:
                options = Options()
            options.add_argument("--headless")
            options.add_argument("--blink-settings=imagesEnabled=false")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")

            # ---- additional options # TODO testing
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-extensions")
            options.add_argument("--proxy-server='direct://'")
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            # options.add_argument("--disable-http2")  # TODO this one is causing program to freeze

            # Randomise the user agents

            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
            ]

            random_user_agent = random.choice(user_agents)
            options.add_argument(f"user-agent={random_user_agent}")

            # Create the webdriver
            driver = uc.Chrome(options=options, service=service)
            driver.maximize_window()

        return driver

    def zenrows_client(self):
        with open("src/config/secrets.toml", "r") as f:
            config = toml.load(f)

        api_key = config["zenrows"]["API_KEY"]
        client = ZenRowsClient(api_key)
        return client

    @abstractmethod
    def process():
        """This method needs to be implemented to orchestrate the end to end
        tasks required to extract, transform and load the data."""
        pass

    def quit(self):
        print("CLOSING WEBDRIVER")
        self.driver.quit()

    # context management
    def __enter__(self):
        print("INITIALISING WEB DRIVER IN CONTEXT MANAGER")
        return self

    def __exit__(self, *exc_info):
        self.quit()
