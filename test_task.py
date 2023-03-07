import json
import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class AutoLankaScraper:
    def __init__(self, search_query, **kwargs):
        self.website = "https://auto-lanka.com"
        self.search_query = search_query

        if kwargs:
            for key, value in kwargs.items():
                self.search_query = self.search_query + "&{}={}".format(key, value)

        self.path = os.environ.get("DRIVER_PATH")
        self.regx_for_date_pattern = "\d{2}\s+\w{3}\s+\d{2}:\d{2}\s+(?:AM|PM)"
        self.driver = self.get_driver()

    def get_driver(self):
        driver_name = os.environ.get("DRIVER_NAME")
        if driver_name == "chrome":
            return self.get_chrome_driver()
        else:
            raise Exception("No driver is defined.")

    def get_chrome_driver(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument("--disable-notifications")

        return webdriver.Chrome(
            chrome_options=self.chrome_options, executable_path=self.path
        )

    def get_data_from_new_tab(self, link):
        item = {}
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)

        print("Now scrapping data for {}...".format(self.driver.title))

        div = self.driver.find_element("id", "ctl00_ContentPlaceHolder1_divCarDetails")
        item["name"] = div.find_element(By.TAG_NAME, "h1").text
        span_text = div.find_element(By.TAG_NAME, "span").text
        posted_on = span_text[
            re.search(self.regx_for_date_pattern, span_text).span()[0] :
        ]
        item["posted_on"] = posted_on
        item["posted_city"] = posted_on.split(" ")[-2].replace(",", "")
        item["price"] = div.find_element(By.CLASS_NAME, "ui-price-tag").text

        short_info = div.find_element(By.CLASS_NAME, "short-info").text.split("\n")

        for data in short_info:
            if data.startswith("Condition:"):
                item["condition"] = data.split(": ")[1]
            elif data.startswith("Model year:"):
                item["year_of_manufacture"] = data.split(": ")[1]

        item["link"] = self.driver.current_url

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        return item

    def search(self):
        url = f"{self.website}/Default.aspx?qry={self.search_query}"
        self.driver.get(url)
        print("Scrapping started!!!")

        result_div = self.driver.find_element_by_class_name("recommended-ads")

        # Check for valid results found or not
        if result_div.find_elements_by_xpath(
            "//h4[contains(text(), 'Sorry, no results found - try a different search.')]"
        ):
            self.driver.quit()
            return json.dumps("No results found")

        links = result_div.find_elements_by_tag_name("a")
        list_of_link_ids = []
        for x in range(len(links)):
            # This logic is to skip the adds
            if links[x].text:
                list_of_link_ids.append(x)
                if len(list_of_link_ids) == 10:
                    break

        list_of_results = []
        for x in list_of_link_ids:
            try:
                dict_of_result = {}
                link = links[x].get_attribute("href")
                data = self.get_data_from_new_tab(link)
                dict_of_result["overview"] = data
                list_of_results.append(dict_of_result)
            except:
                print("Error occurred while scraping data!!!")

        print("Scrapping completed!!!")

        self.driver.quit()
        return json.dumps(list_of_results, indent=4)


search_query = "cars"
scraper = AutoLankaScraper(search_query, model="honda")
results = scraper.search()
print(results)
