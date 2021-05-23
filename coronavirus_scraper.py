import requests
from typing import Union

from datetime import date
from bs4 import BeautifulSoup  # type: ignore
from csv import writer
from time import sleep

# I live in Tokyo and my family lives in Dayton, Ohio in the USA, so sometimes
# it's hard to keep track of the coronavirus situation back home.  I wrote this
# script to keep a record of coronavirus cases both here in Tokyo and in Dayton.

# I automate this script to run automatically each day with Task Scheduler on Windows.
# For viewing the data, run the separate coronavirus_reader.py script.

# For my purposes I define Dayton as two counties; Montgomery and Greene.


# str_or_int variable is for type checking; most values will be ints except when the scraper doesn't find any values,
# at which point it will return the string 'NULL'
str_or_int = Union[str, int]


class COVID19_Scraper:
    def __init__(self) -> None:
        self.date = date.today()

    @staticmethod
    def get_dayton_stats() -> str_or_int:
        # Dayton information is taken from two separate pages on the New York Times site, so this function finds
        # the case number for each county and strips unnecessary information from each
        def nytimes_scraper(url):
            ohio_response = requests.get(url)
            ohio_soup = BeautifulSoup(ohio_response.text, "html.parser")
            return int(ohio_soup.find(id="cases").find_all("strong")[1].get_text().replace(" cases per day", ""))

        new_greene_cases = nytimes_scraper("https://www.nytimes.com/interactive/2021/us/greene-ohio-covid-cases.html")
        sleep(1)
        new_montgomery_cases = nytimes_scraper("https://www.nytimes.com/interactive/2021/us/montgomery-ohio-covid-cases.html")

        dayton_total = new_greene_cases + new_montgomery_cases

        # If the totals have not yet been updated, this will return the string "NULL"
        if dayton_total == 0:
            return "NULL"
        return dayton_total

    @staticmethod
    def get_tokyo_stats() -> str_or_int:
        url = "https://stopcovid19.metro.tokyo.lg.jp/en"
        tokyo_response = requests.get(url)
        tokyo_soup = BeautifulSoup(tokyo_response.text, "html.parser")

        tokyo_total = int(tokyo_soup.find(class_="InfectionMedicalcareprovisionStatus-description").span.get_text().replace("人", "").replace(",", ""))

        if tokyo_total == 0:
            return "NULL"
        return tokyo_total

    @staticmethod
    def package_data(dayton_total: str_or_int, tokyo_total: str_or_int) -> dict:
        today = date.today().strftime("%d-%m-%y")
        return {"Date": today, "Dayton": dayton_total, "Tokyo": tokyo_total}

    @staticmethod
    def write_to_csv(date: str, new_dayton_cases: str_or_int, new_tokyo_cases: str_or_int) -> None:
        # Records the number of new cases in Dayton and Tokyo into a csv file called coronavirus_data.csv
        with open("coronavirus_data.csv", "a", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerow([date, new_dayton_cases, new_tokyo_cases])

    @staticmethod
    def main() -> None:
        scraper = COVID19_Scraper()
        todays_values = scraper.package_data(scraper.get_dayton_stats(), scraper.get_tokyo_stats())
        scraper.write_to_csv(todays_values["Date"], todays_values["Dayton"], todays_values["Tokyo"])


if __name__ == "__main__":
    COVID19_Scraper.main()
