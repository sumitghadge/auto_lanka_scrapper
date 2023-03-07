# AutoLankaScraper

AutoLankaScraper is a Python class used to scrape data from the AutoLanka website (https://auto-lanka.com). The class uses the Selenium webdriver to navigate to the search results page and then extract data for the specified search query. The extracted data includes the name of the car, the posted date, the posted city, the price, the condition, the year of manufacture, and the link to the car details page. The data is returned as a JSON string.

## Dependencies
* Python 3.x
* Selenium
* Chrome webdriver

## Usage
1. Install the dependencies from requirements.txt file.
2. Set the `DRIVER_PATH` and `DRIVER_NAME` environment variable to the path of the Chrome webdriver executable.
3. Create an instance of the AutoLankaScraper class, passing the search query as the first argument. You can also pass keyword arguments.
4. Call the `search` method on the AutoLankaScraper instance to initiate the search and scrape the data.

Example usage:
```
search_query = "cars"
scraper = AutoLankaScraper(search_query, model="honda")
results = scraper.search()
print(results)
```

Note: Make sure to replace the `model` parameter with the appropriate one.