import time, sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

total_count = 35 

def inf_scroll():
	print("0")
	reviews = driver.find_elements(By.CLASS_NAME, "jxjCjc")
 	prev = 0
 	while ((len(reviews) < total_count) and (prev!=len(reviews))):
 		print("1")
 		driver.execute_script("arguments[0].scrollIntoView(true);", reviews[-1])
 		time.sleep(1)
 		prev = len(reviews)
 		reviews = driver.find_elements(By.CLASS_NAME, "jxjCjc")
 	return reviews

def Collect(cat_in):
	global stars, text, cat
	reviews = inf_scroll()
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

		# Collect Textual Review
		text.append(i.find_element(By.CLASS_NAME, "Jtu6Td").text)

		# Category
		cat.append(cat_in)
		if cat_in == "Relevent":
			text =text[ :total_count]
			cat = cat[ :total_count]
			stars = stars[ :total_count]
		else: 
			text =text[ :2*total_count]
			cat = cat[ :2*total_count]
			stars = stars[ :2*total_count]

# Loading Google-chrome driver
driver = webdriver.Chrome(r"/home/rishabh/Desktop/EY/chromedriver")
# Name of the outlet is supposed to be a command line arg
dealer_mas = sys.argv[1]

# URL represetning the required google search
url = 'https://www.google.com/search?q={}'.format(dealer_mas)
driver.get(url)

# Click on "View all Reviews"
buttons = driver.find_element(By.CLASS_NAME, "qB0t4").find_element(By.TAG_NAME, "a")
buttons.click()
time.sleep(1) # wait for Loading
# inf_scroll()

# Collecting all Reviews
stars, text, cat = [], [], []
Collect("Relavent")

# Newest
driver.refresh()
time.sleep(3)
# exit(0)
Sort_By = driver.find_elements(By.CLASS_NAME, "AxAp9e")
for i in Sort_By:
	if i.get_attribute('data-sort-id') == "newestFirst" :
		i.click() #CLick on Newest First
		time.sleep(1) #wait for loading
		Collect("Newest")
		break

driver.close()

# Generate DataFrame and save CSV
Df = pd.DataFrame([text, stars, cat]).T
Df.columns=["Text", "Rating", "Category"]
fin_name = dealer_mas.replace("\\", "").replace("/", "")
Df.to_csv("output/" + "_".join(fin_name.split()) + ".csv")
