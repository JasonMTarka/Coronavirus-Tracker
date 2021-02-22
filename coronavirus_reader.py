from csv import reader
import re

with open("coronavirus_data.csv") as file:
	csv_reader = reader(file)
	data = list(csv_reader)

today = data[len(data)-1]

#yesterday = data[len(data)-2]
# Above code is in case you want to see yesterday's data. 

# Below is a regex which will match the day, month, and year that the data was collected.

date_analysis = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d\d?)")
match = date_analysis.search(today[0])

# Below converts the regex groups into variables so that they can be included in the final f-string.

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

month = MONTHS[match.group("month")]
day = match.group("day")
year = match.group("year")

tokyo_new_cases = today[2]
dayton_new_cases = today[1]

print(f"The number of new cases in Tokyo on {month} {day}, {year} was {tokyo_new_cases}.")
print(f"The number of new cases in Dayton was {dayton_new_cases}.")
