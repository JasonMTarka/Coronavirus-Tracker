import unittest
import requests
from bs4 import BeautifulSoup

from coronavirus_scraper import COVID19_Scraper

class TestScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        scraper = COVID19_Scraper()
        cls.todays_values = scraper.package_data(scraper.get_dayton_stats(), scraper.get_tokyo_stats())

    def test_scraper(self):
        self.assertIsNotNone(self.todays_values.get("Date"))
        self.assertIsNotNone(self.todays_values.get("Dayton"))
        self.assertIsNotNone(self.todays_values.get("Tokyo"))

    def test_tokyo(self):
        url = "https://stopcovid19.metro.tokyo.lg.jp/en"
        tokyo_response = requests.get(url)
        tokyo_soup = BeautifulSoup(tokyo_response.text, "html.parser")
        self.assertIsNotNone(tokyo_soup.find(class_="InfectionMedicalCareProvisionStatus-description"))


if __name__ == "__main__":
    unittest.main()
