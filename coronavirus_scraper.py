import requests
import logging

from typing import Union
from datetime import date
from bs4 import BeautifulSoup
from csv import writer
from time import sleep

# I live in Tokyo and my family lives in Dayton, Ohio in the USA, so sometimes
# it's hard to keep track of the coronavirus situation back home.  I wrote this
# script to keep a record of coronavirus cases both here in Tokyo and in Dayton.

# I automate this script to run automatically each day with Task Scheduler on Windows.
# For viewing the data, run the separate coronavirus_reader.py script.

# For my purposes I define Dayton as two counties; Montgomery and Greene.


# STR_OR_INT variable is for type checking; most values will be ints except when the scraper doesn't find any values,
# at which point it will return the string 'NULL'


class COVID19_Scraper:

    STR_OR_INT = Union[str, int]

    def __init__(self) -> None:

        def logger_setup() -> logging.Logger:

            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

            file_handler = logging.FileHandler('coronavirus_scraper_logs.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            return logger

        self.logger = logger_setup()
        self.date = date.today()

    def main(self) -> None:
        todays_values = self.package_data(self.get_dayton_stats(), self.get_tokyo_stats())
        self.write_to_csv(todays_values["Date"], todays_values["Dayton"], todays_values["Tokyo"])

    def get_dayton_stats(self) -> STR_OR_INT:
        # Dayton information is taken from two separate pages on the New York Times site, so this function finds
        # the case number for each county and strips unnecessary information from each
        def nytimes_scraper(url):
            self.logger.info(f"Beginning to scrape New York Times at {url}...")
            ohio_response = requests.get(url)
            ohio_soup = BeautifulSoup(ohio_response.text, "html.parser")
            self.logger.info("New York Times scraping completed!")
            return int(ohio_soup.find(id="cases").find_all("strong")[1].get_text().replace(" cases per day", ""))

        new_greene_cases = nytimes_scraper("https://www.nytimes.com/interactive/2021/us/greene-ohio-covid-cases.html")
        sleep(1)
        new_montgomery_cases = nytimes_scraper("https://www.nytimes.com/interactive/2021/us/montgomery-ohio-covid-cases.html")

        dayton_total = new_greene_cases + new_montgomery_cases

        # If the totals have not yet been updated, this will return the string "NULL"
        if dayton_total == 0:
            self.logger.warning("No new cases reported.  Returning 'NULL'.")
            return "NULL"
        self.logger.info(f"Dayton totals calculated: {dayton_total}")
        return dayton_total

    def get_tokyo_stats(self) -> STR_OR_INT:
        self.logger.info("Beginning to scrape Tokyo statistics...")
        url = "https://stopcovid19.metro.tokyo.lg.jp/en"
        tokyo_response = requests.get(url)
        tokyo_soup = BeautifulSoup(tokyo_response.text, "html.parser")
        tokyo_total = int(tokyo_soup.find(class_="InfectionMedicalCareProvisionStatus-description").span.get_text().replace("人", "").replace(",", ""))
        self.logger.info("Tokyo scraping completed!")

        if tokyo_total == 0:
            self.logger.warning("No new cases reported.  Returning 'NULL'.")
            return "NULL"
        self.logger.info(f"Tokyo totals calculated: {tokyo_total}")
        return tokyo_total

    def package_data(self, dayton_total: STR_OR_INT, tokyo_total: STR_OR_INT) -> dict:
        today = date.today().strftime("%d-%m-%y")
        return {"Date": today, "Dayton": dayton_total, "Tokyo": tokyo_total}

    def write_to_csv(self, date: str, new_dayton_cases: STR_OR_INT, new_tokyo_cases: STR_OR_INT) -> None:
        # Records the number of new cases in Dayton and Tokyo into a csv file called coronavirus_data.csv
        self.logger.info(f"Recording new data to CSV...")
        with open("coronavirus_data.csv", "a", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerow([date, new_dayton_cases, new_tokyo_cases])


def main():
    scraper = COVID19_Scraper()
    scraper.main()


if __name__ == "__main__":
    main()
