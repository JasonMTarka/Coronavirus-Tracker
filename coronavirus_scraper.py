import requests
import logging
import sys

from datetime import date
from bs4 import BeautifulSoup
from csv import writer
from time import sleep

"""
I live in Tokyo and my family lives in Dayton, Ohio in the USA, so sometimes
it's hard to keep track of the coronavirus situation back home.  I wrote this
script to keep a record of coronavirus cases both here in Tokyo and in Dayton.

I automate this script to run automatically each day with Task Scheduler.
For viewing the data, run the separate coronavirus_reader.py script.

For my purposes I define Dayton as two counties; Montgomery and Greene.

STR_OR_INT variable is for type checking; most values will be ints except when
 the scraper doesn't find any values, at which point it will return
 the string 'NULL'
"""


class COVID19_Scraper:
    """Object for scraping coronavirus data."""

    STR_OR_INT = str | int

    def __init__(self) -> None:
        """Set today's data and create logger object."""

        def logger_setup() -> logging.Logger:
            """Instantiate and format logger object."""

            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
            )

            file_handler = logging.FileHandler("coronavirus_scraper_logs.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            return logger

        self.logger = logger_setup()
        self.date = date.today()

    def main(self) -> None:
        """Primary method to get data and then write it to csv."""

        todays_values = self.package_data(
            self.get_dayton_stats(), self.get_tokyo_stats()
        )
        self.write_to_csv(
            todays_values["Date"],
            todays_values["Dayton"],
            todays_values["Tokyo"],
        )

    def get_dayton_stats(self) -> STR_OR_INT:
        """Finds the case number for each county comprising Dayton and strips
        unnecessary information from each."""

        def nytimes_scraper(url):
            """Get data from New York Times url."""

            self.logger.info(f"Beginning to scrape New York Times at {url}...")
            ohio_response = requests.get(url)
            ohio_soup = BeautifulSoup(ohio_response.text, "html.parser")
            self.logger.info("New York Times scraping completed!")
            return int(
                ohio_soup.find(id="cases")
                .find_all("strong")[1]
                .get_text()
                .replace(" cases per day", "")
            )

        new_greene_cases = nytimes_scraper(
            "https://www.nytimes.com/interactive/2021/us/greene-ohio-covid-cases.html"
        )

        sleep(1)

        new_montgomery_cases = nytimes_scraper(
            "https://www.nytimes.com/interactive/2021/us/montgomery-ohio-covid-cases.html"
        )

        dayton_total = new_greene_cases + new_montgomery_cases

        if dayton_total == 0:
            self.logger.warning("No new cases reported.  Returning 'NULL'.")
            return "NULL"
            # Return the string "NULL" if today's cases are not yet updated.

        self.logger.info(f"Dayton totals calculated: {dayton_total}")
        return dayton_total

    def get_tokyo_stats(self) -> STR_OR_INT:
        """Scrape Tokyo data from official website."""

        self.logger.info("Beginning to scrape Tokyo statistics...")
        url = "https://stopcovid19.metro.tokyo.lg.jp/en"
        tokyo_response = requests.get(url)
        tokyo_soup = BeautifulSoup(tokyo_response.text, "html.parser")

        try:
            tokyo_total = int(
                tokyo_soup.find(
                    class_="InfectionMedicalCareProvisionStatus-description"
                )
                .em.contents[0]
                .replace(" ", "")
                .replace("\n", "")
                .replace(",", "")
            )
        except ValueError as e:
            self.logger.error(f"Value Error: {e}")
            sys.exit()
        except Exception as e:
            self.logger.error(f"Exception: {e}")
            sys.exit()

        self.logger.info("Tokyo scraping completed!")

        if tokyo_total == 0:
            self.logger.warning("No new cases reported.  Returning 'NULL'.")
            return "NULL"
        self.logger.info(f"Tokyo totals calculated: {tokyo_total}")
        return tokyo_total

    def package_data(
        self, dayton_total: STR_OR_INT, tokyo_total: STR_OR_INT
    ) -> dict:
        """Format data into readable format."""

        today = date.today().strftime("20%y/%m/%d")
        return {"Date": today, "Dayton": dayton_total, "Tokyo": tokyo_total}

    def write_to_csv(
        self,
        date: str,
        new_dayton_cases: STR_OR_INT,
        new_tokyo_cases: STR_OR_INT,
    ) -> None:
        """Record number of new cases in Dayton and Tokyo to csv."""

        self.logger.info(f"Recording new data to CSV...")

        with open("coronavirus_data.csv", "a", newline="") as file:
            new_row = [date, new_dayton_cases, new_tokyo_cases]
            self.logger.info(f"New row: {new_row}")
            csv_writer = writer(file)
            csv_writer.writerow(new_row)


def main():
    """Initialize COVID19_Scraper object and begin main loop."""

    scraper = COVID19_Scraper()
    scraper.main()


if __name__ == "__main__":
    main()
