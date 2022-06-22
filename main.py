from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

URL ="https://www.zillow.com/san-francisco-ca/rentals/1-_beds/1.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417331103516%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.68853875977319%2C%22north%22%3A37.86194346849393%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
response = requests.get(url=URL, headers={'Accept-Language':'en-US,en;q=0.9',
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
housing_web_page = response.text

soup = BeautifulSoup(housing_web_page,"html.parser")
prices = soup.find_all(name="div", class_="list-card-price")
addresses = soup.find_all(name="address", class_="list-card-addr")
house_links = soup.find_all(name='a', class_="list-card-link")

prices_text =[]
addresses_text =[]
house_links_text =[]

for price_tag in prices:
    price_text = price_tag.getText()
    if "+" or "/" in price_text:
        price_text = price_text.split("/")[0]
        price_text = price_text.split("+")[0]
        prices_text.append(price_text)
    else:
        prices_text.append(price_text)

for address_tag in addresses:
    text = address_tag.getText()
    addresses_text.append(text)

for link_tag in house_links:
    link = link_tag.get("href")
    if "https://" not in link:
        link = f"https://www.zillow.com{link}"
        house_links_text.append(link)
    else:
         house_links_text.append(link)

#remove the duplicated item and keep the orginal order
clean_house_links_text = list(dict.fromkeys(house_links_text))

print(prices_text)
print(addresses_text)
print(clean_house_links_text)

#input data into google form

chrome_drive_path ="C:\Development\chromedriver.exe"
srv = Service(chrome_drive_path)
driver = webdriver.Chrome(service=srv)
driver.get("https://forms.gle/EbJg7TZBsCRsYhx19")

for n in range(len(addresses_text)):

    input_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_address.send_keys(addresses_text[n])

    input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_price.send_keys(prices_text[n])

    input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_link.send_keys(clean_house_links_text[n])

    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span' )
    submit_btn.click()

    submit_another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another.click()
    time.sleep(2)

