import numpy as np
import re

from csv import reader
from matplotlib import pyplot as plt


class COVID19_Reader:
    """Class which prints to terminal and/or displays a Matplotlib graph."""

    def __init__(self) -> None:
        """Initialize self.data as an empty list."""

        self.data: list = []

    def data_reader(self) -> None:
        """Read data from coronavirus_data.csv and set self.data to it."""

        with open("coronavirus_data.csv") as file:
            csv_reader = reader(file)
            self.data = list(csv_reader)

    def print_cases(self) -> None:
        """Print self.data information to the console."""

        todays_data = self.data[len(self.data) - 1]
        # self.data[len(self.data)-2]
        # The above commented out code allows access to yesterday's data.

        # Below is a regex which will match the day, month, and year.
        regex = r"(?P<year>\d{2})-(?P<month>\d{2})-(?P<day>\d\d?)"
        date_analysis: re.Pattern[str] = re.compile(regex)
        match: re.Match[str] = (
            date_analysis.search(todays_data[0]))  # type: ignore
        """
        If above is not type: ignore'd, mypy returns:
        error: Incompatible types in assignment
        (expression has type "Optional[Match[Any]]",
        variable has type "Match[Any]")
        expected solution of 'assert date_analysis is not None'
        does not change the above error
        """

        MONTHS = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }

        month = MONTHS[match.group("month")]
        day = match.group("day")
        year = "20" + match.group("year")

        tokyo_new_cases = todays_data[2]
        dayton_new_cases = todays_data[1]
        print(
            f"The number of new cases in Tokyo on {month} {day}, {year}"
            f" was {tokyo_new_cases}.\n"
            f"The number of new cases in Dayton was {dayton_new_cases}.")

    def graph(self) -> None:
        """Graph data stored in self.data."""

        plt.style.use("ggplot")
        plt.xlabel("Dates")
        plt.ylabel("Number of New Cases")
        plt.title("Number of Coronavirus Cases in Dayton and Tokyo")

        x_dates = []
        y_cases_dayton = []
        y_cases_tokyo = []

        for row in self.data[1:]:
            x_dates.append(row[0])
            if row[1] != "NULL":
                y_cases_dayton.append(int(row[1]))
            else:
                y_cases_dayton.append(0)
            if row[2] != "NULL":
                y_cases_tokyo.append(int(row[2]))
            else:
                y_cases_tokyo.append(0)

        x_indexes = np.arange(len(x_dates))
        # Creates a numpy array which contains the indexes of the dates,
        # using the indexes to display the data instead of the data itself

        plt.plot(x_dates, y_cases_dayton, marker="o", label="Dayton")
        plt.plot(x_dates, y_cases_tokyo, marker="o", label="Tokyo")

        plt.xticks(ticks=x_indexes, labels=x_dates)
        # Sets ticks equal to indexes

        plt.locator_params(axis="x", nbins=5)
        # Sets the amount of x labels which display

        plt.legend()
        plt.tight_layout()
        plt.show()


def main() -> None:
    """Initialize COVID19_Reader() object and call print and graph methods."""

    cvd_reader = COVID19_Reader()
    cvd_reader.data_reader()

    # cvd_reader.print_cases()
    cvd_reader.graph()


if __name__ == "__main__":
    main()
