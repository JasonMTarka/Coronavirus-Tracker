from csv import reader
from matplotlib import pyplot as plt
import numpy as np
import re

class COVID19_Reader:
	def __init__(self):
		self.data = []

	def data_reader(self):
		with open("coronavirus_data.csv") as file:
			csv_reader = reader(file)
			self.data = list(csv_reader)
			return self.data
	
	def print_cases(self, data):
		todays_data = data[len(data)-1] #data[len(data)-2]
		# The above commented out code allows you to see yesterday's data instead.

		# Below is a regex which will match the day, month, and year that the data was collected.
		date_analysis = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d\d?)")
		match = date_analysis.search(todays_data[0])
		MONTHS = {
			"01" : "January",
			"02" : "February",
			"03" : "March",
			"04" : "April",
			"05" : "May",
			"06" : "June",
			"07" : "July",
			"08" : "August",
			"09" : "September",
			"10" : "October",
			"11" : "November",
			"12" : "December"
		}

		# Below converts the regex groups into variables so that they can be included in the final f-string.
		month = MONTHS[match.group("month")]
		day = match.group("day")
		year = match.group("year")

		tokyo_new_cases = todays_data[2]
		dayton_new_cases = todays_data[1]
		print(f"The number of new cases in Tokyo on {month} {day}, {year} was {tokyo_new_cases}.")
		print(f"The number of new cases in Dayton was {dayton_new_cases}.")

	def graph(self, data):
		plt.style.use("ggplot")
		plt.xlabel("Dates") 
		plt.ylabel("Number of New Cases") 
		plt.title("Number of Coronavirus Cases in Dayton and Tokyo")
		
		x_dates = []
		y_cases_dayton = []
		y_cases_tokyo = []

		for row in data[1:]:
			x_dates.append(row[0])
			if row[1] != "NULL":
				y_cases_dayton.append(int(row[1]))
			else:
				y_cases_dayton.append(0)
			if row[2] != "NULL":
				y_cases_tokyo.append(int(row[2]))
			else:
				y_cases_tokyo.append(0)	

		x_indexes = np.arange(len(x_dates)) # Creates a numpy array which contains the indexes of the dates, using the indexes to display the data instead of the data itself

		plt.plot(x_dates, y_cases_dayton, marker="o", label="Dayton") 
		plt.plot(x_dates, y_cases_tokyo, marker="o", label="Tokyo")

		plt.xticks(ticks=x_indexes, labels=x_dates) # Sets ticks equal to indexes
		plt.locator_params(axis="x", nbins=5) # Sets the amount of x labels which display

		plt.legend()
		plt.tight_layout()
		plt.show()

if __name__ == "__main__":	
	cvd_reader = COVID19_Reader()
	data = cvd_reader.data_reader()

	cvd_reader.print_cases(data)
	cvd_reader.graph(data)
