import unittest

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


if __name__ == "__main__":
    unittest.main()
