import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# URL of the HKJC racing data page


def get_racing_data(url):
    # Send a GET request to the URL
    dr = webdriver.Chrome()
    dr.get(url)
    time.sleep(1)

    # Create a BeautifulSoup object to parse the HTML content
    bs = BeautifulSoup(dr.page_source, "lxml")

    # Find the table containing the racing data
    table = bs.find("table", {"class": "f_tac table_bd draggable"})

    racing_data = []
    if table == None:
        return None
    else:
        # Extract the rows from the table
        rows = table.find_all("tr")

    # Iterate over the rows
        for row in rows:
            # Find the columns in each row
            columns = row.find_all("td")

        # Extract the data from the columns and append it to the racing_data list
            data = [column.text.strip() for column in columns]
            racing_data.append(data)

        return racing_data


def scrape_all_racing_data(date):
    base_url = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate="+date+"&RaceNo="
    current_page = 1
    all_racing_data = []

    while True:
        url = base_url + str(current_page)
        racing_data = get_racing_data(url)

        if racing_data:
            all_racing_data.extend(racing_data)
            current_page += 1
        else:
            break

    return all_racing_data


def scrape_all_racing_date():
    url = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx"
    dr = webdriver.Chrome()
    dr.get(url)
    time.sleep(1)
    bs = BeautifulSoup(dr.page_source, "lxml")
    Alldate = bs.find("select", {"id": "selectId"})
    rows = Alldate.find_all("option")
    values = [date["value"] for date in rows if date["value"]]
    print(values)
    print("\n")


print("Listed all racing date\n")
scrape_all_racing_date()
print("-----------------------\n")
# Input date
date = input("Please enter the race date. YYYY/MM/DD?\n")

# Call the function to get the racing data
data = scrape_all_racing_data(date)

# Specify the output file name
output_file = "racing_data.csv"

# Save the racing data as a CSV file

with open(output_file, "w", newline="", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print(f"All racing data has been saved as {output_file}.")
