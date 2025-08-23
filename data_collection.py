import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize driver
driver = webdriver.Chrome()
url = "https://www.cars24.com/buy-used-petrol-cars-new-delhi/?sort=bestmatch&serveWarrantyCount=true&listingSource=TabFilter&storeCityId=2"
driver.get(url)

# Scroll to load all content
scroll_pause_time = 0.1
step = 300
scroll_height = driver.execute_script("return document.body.scrollHeight")
current_position = 0

while current_position < scroll_height:
    driver.execute_script(f"window.scrollTo(0, {current_position});")
    time.sleep(scroll_pause_time)
    current_position += step
    scroll_height = driver.execute_script("return document.body.scrollHeight")

# Parse page
soup = BeautifulSoup(driver.page_source, "html.parser")
time.sleep(15)
driver.quit()

# Initialize lists
Dom, company, model, odometer_reading, fuel_type, transmission, RTo, price = [], [], [], [], [], [], [], []

# Each car container
cars = soup.find_all('div', class_='styles_outer__NTVth')

for car in cars:
    # Car title: Dom, Company, Model
    title_tag = car.find('span', class_='sc-braxZu kjFjan')
    if title_tag:
        text = title_tag.text.split(" ")
        Dom.append(text[0])
        company.append(text[1])
        model.append(' '.join(text[2:]))
    else:
        Dom.append(None)
        company.append(None)
        model.append(None)

    # Car details: odometer, fuel, transmission, RTO
    details = car.find_all('p', class_='sc-braxZu kvfdZL')
    if len(details) == 4:
        odometer_reading.append(details[0].text)
        fuel_type.append(details[1].text)
        transmission.append(details[2].text)
        RTo.append(details[3].text)
    else:
        odometer_reading.append(None)
        fuel_type.append(None)
        transmission.append(None)
        RTo.append(None)

    # Price
    price_tag = car.find('p', class_='sc-braxZu cyPhJl')
    if price_tag:
        price.append(price_tag.text)
    else:
        price.append(None)

# Verify lengths
print(f"length of Dom : {len(Dom)}")
print(f"length of comp : {len(company)}")
print(f"length of model : {len(model)}")
print(f"length of odometer_reading : {len(odometer_reading)}")
print(f"length of fuel : {len(fuel_type)}")
print(f"length of transmission : {len(transmission)}")
print(f"length of RTO : {len(RTo)}")
print(f"length of price : {len(price)}")

# Save to CSV
df = pd.DataFrame({
    "YOM": Dom,
    "Company": company,
    "Model": model,
    "Odometer": odometer_reading,
    "Fuel": fuel_type,
    "Transmission": transmission,
    "RTO": RTo,
    "Price": price
})
df.to_csv("car_data4.csv", index=False)
