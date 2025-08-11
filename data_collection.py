import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 

driver  = webdriver.Chrome()
url = "https://www.cars24.com/buy-used-hybrid-cars-new-delhi/?sort=bestmatch&serveWarrantyCount=true&listingSource=TabFilter&storeCityId=2"
driver.get(url)
scroll_pause_time = 0.1  # seconds
scroll_height = driver.execute_script("return document.body.scrollHeight")
current_position = 0
step = 300  # pixels per scroll

while current_position < scroll_height:
    driver.execute_script(f"window.scrollTo(0, {current_position});")
    time.sleep(scroll_pause_time)
    current_position += step
    scroll_height = driver.execute_script("return document.body.scrollHeight")  # update in case new content loads

soup = BeautifulSoup(driver.page_source,"html.parser")
time.sleep(22)
driver.close()

# init the lists 
Dom ,company,model, odometer_reading,fuel_type,transmission,RTo= [],[],[],[],[],[],[]

# getting the name, model and manufacture of the car 
for i in soup.find_all('span',class_ ='sc-braxZu kjFjan'):
    text = i.text.split(" ")
    Dom.append(text[0])
    company.append(text[1])
    model.append(' '.join(text[2:]))

# loading the container info of the page. 
car_info = soup.find_all('div',class_ ='styles_outer__NTVth' )
data = []

# loading all the info in data 
for i in car_info:
    for tag in i.find_all('p', class_="sc-braxZu kvfdZL"):
        data.append(tag.text)

# seprating the data into its corresponding list 

for idx ,item in enumerate(data,start=1):
    if idx % 4 == 1:
        odometer_reading.append(item)
    elif idx % 4 ==2:
            fuel_type.append(item)
    elif idx % 4 ==3:
        transmission.append(item)
    else:
        RTo.append(item)

    
print(f"length of Dom : {len(Dom)}")
print(f"length of comp : {len(company)}")
print(f"length of model : {len(model)}")
print(f"length of odometer_reading : {len(odometer_reading)}")
print(f"length of fuel : {len(fuel_type)}")
print(f"length of transmission : {len(transmission)}")
print(f"length of RTO : {len(RTo)}")

import pandas as pd

df= pd.DataFrame({
    "YOM": Dom,
    "Company":company,
    "Model":model,
    "odometer": odometer_reading,
    "fuel":fuel_type,
    "transmission": transmission,
    "RTO":RTo
})
df.to_csv("car_data4.csv",index=False)



