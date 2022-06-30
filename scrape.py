import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def inf_scroll():
	SCROLL_PAUSE_TIME = 0.5

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    # Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


driver = webdriver.Chrome(r"/home/rishabh/Desktop/EY/chromedriver")
# dealer_mas =  input("Enter Dealer Name")
dealer_mas = 'pasco house plot number 6, old delhi gurgaon road, industrial estate,sector 18, gurugram, haryana, 122015'
# dealer_mas = "T R SAWHNEY MOTORS PVT. LTD. 9-10 /3 ,LAXMAN HOUSE"

url = 'https://www.google.com/search?q={}'.format(dealer_mas + "google maps")
# url = "https://www.google.com/maps/search?q={}".format(dealer_mas)
# print(url)
driver.get(url)


buttons = driver.find_element(By.CLASS_NAME, "qB0t4").find_element(By.TAG_NAME, "a")
buttons.click()
time.sleep(1)
# inf_scroll()
reviews = driver.find_elements(By.CLASS_NAME, "jxjCjc")
stars, text = [], []
for i in reviews:
	# to remove the "... More"
	try:
		i.find_element(By.CLASS_NAME, "review-more-link").click()
	except:
		pass

	# Collect Star(0-5) Value
	star = i.find_element(By.CLASS_NAME, "PuaHbe")
	star = star.find_element(By.TAG_NAME, "span")
	star = star.get_attribute('aria-label')
	stars.append(float(star.split()[1]))

	# Collect Actual Review
	text.append(i.find_element(By.CLASS_NAME, "Jtu6Td").text)

driver.close()
Df = pd.DataFrame([text, stars]).T
Df.columns=["Text", "Rating"]
Df.to_csv("Reviews_" + "_".join(dealer_mas.split()) + ".csv")
print(Df.head())
