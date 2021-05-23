import numpy as np
import re

from csv import reader
from matplotlib import pyplot as plt  # type: ignore
# If above is not type: ignore, mypy returns:
# error: Skipping analyzing 'matplotlib': found module but no type hints or library stubs


class COVID19_Reader:
    def __init__(self) -> None:
        self.data: list = []

    def data_reader(self) -> list:
        with open("coronavirus_data.csv") as file:
            csv_reader = reader(file)
            self.data = list(csv_reader)
            return self.data

    def print_cases(self) -> None:
        todays_data = self.data[len(self.data) - 1]  # self.data[len(self.data)-2]
        # The above commented out code allows you to see yesterday's data instead.

        # Below is a regex which will match the day, month, and year that the data was collected.
        date_analysis: re.Pattern = re.compile(r"(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d\d?)")
        match: re.Match = date_analysis.search(todays_data[0])  # type: ignore
        # If above is not type: ignore, mypy returns:
        # error: Incompatible types in assignment (expression has type "Optional[Match[Any]]", variable has type "Match[Any]")

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

        # Below converts the regex groups into variables so that they can be included in the final f-string.
        month = MONTHS[match.group("month")]
        day = match.group("day")
        year = "20" + match.group("year")

        tokyo_new_cases = todays_data[2]
        dayton_new_cases = todays_data[1]
        print(f"The number of new cases in Tokyo on {month} {day}, {year} was {tokyo_new_cases}.")
        print(f"The number of new cases in Dayton was {dayton_new_cases}.")

    def graph(self) -> None:
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

        x_indexes = np.arange(len(x_dates))  # Creates a numpy array which contains the indexes of the dates, using the indexes to display the data instead of the data itself

        plt.plot(x_dates, y_cases_dayton, marker="o", label="Dayton")
        plt.plot(x_dates, y_cases_tokyo, marker="o", label="Tokyo")

        plt.xticks(ticks=x_indexes, labels=x_dates)  # Sets ticks equal to indexes
        plt.locator_params(axis="x", nbins=5)  # Sets the amount of x labels which display

        plt.legend()
        plt.tight_layout()
        plt.show()


def main() -> None:
    cvd_reader = COVID19_Reader()
    cvd_reader.data_reader()

    cvd_reader.print_cases()
    cvd_reader.graph()


if __name__ == "__main__":
    main()
