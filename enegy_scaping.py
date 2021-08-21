from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.maximize_window()

# move to kepco page
url = "https://pp.kepco.co.kr/"
browser.get(url)

# input id, pw
browser.find_element_by_id("RSA_USER_ID").send_keys("071005****")
browser.find_element_by_id("RSA_USER_PWD").send_keys("blurred")

# click login button
browser.find_element_by_class_name("intro_btn").click()

# move to daily peak page
browser.implicitly_wait(20)
browser.get("https://pp.kepco.co.kr/rs/rs0102.do?menu_id=O010202")
time.sleep(2)
browser.implicitly_wait(20)
time.sleep(5)
browser.find_element_by_id("kW").click()
time.sleep(1)

# save as .csv file
import csv
import requests
from bs4 import BeautifulSoup
soup = BeautifulSoup(browser.page_source, "lxml")

filename = "daily_energy_peak.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "일자   최대수요(kW)".split("\t")
writer.writerow(title)

data_rows = soup.find("table", attrs={"class":"ui-jqgrid-btable"}).find("tbody").find_all("tr")
for row1 in data_rows[1:]:
    columns = row1.find_all("td")
    data = [column.get_text() for column in columns][0:2]
    writer.writerow(data)

for row2 in data_rows[1:]:
    columns = row2.find_all("td")
    data = [column.get_text() for column in columns][4:6]
    writer.writerow(data)

browser.quit()