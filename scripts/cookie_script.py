from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pyautogui  # For moving mouse slightly

# Setup Chrome
options = Options()
options.add_argument("--start-maximized")

# Path to your chromedriver
path = '/Users/aadhithkumaresan/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)

# Open Facebook
driver.get("https://www.facebook.com")
time.sleep(3)

# Inject cookies (already logged-in ones)
cookies = [
    {"name": "c_user", "value": "100022773974406"},
    {"name": "xs", "value": "25%3AjT9OdBMg-XmvPA%3A2%3A1745852939%3A-1%3A4410%3A%3AAcUQqmnVI_Y-LiWGMJtuk-atk9RIztWMNHesJx_7RA"},
]

for cookie in cookies:
    driver.add_cookie(cookie)

# Refresh and go to Marketplace Vehicles page
driver.refresh()
time.sleep(5)
driver.get("https://www.facebook.com/marketplace/halifax/vehicles")
time.sleep(5)

print("✅ Successfully logged into Facebook Marketplace!")

# Scroll to load all posts
previous_height = driver.execute_script("return document.body.scrollHeight")
scroll_attempts = 0
max_scroll_attempts = 30

while scroll_attempts < max_scroll_attempts:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)
    current_height = driver.execute_script("return document.body.scrollHeight")
    
    # Move mouse slightly to prevent screen sleep
    pyautogui.moveRel(5, 0)
    pyautogui.moveRel(-5, 0)

    if current_height == previous_height:
        scroll_attempts += 1
        print(f"⚡ No new posts loaded. Same height detected {scroll_attempts} times.")
    else:
        scroll_attempts = 0
    previous_height = current_height

print("✅ Finished scrolling.")

# Find all vehicle listings
posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/marketplace/item/")]')

print(f"✅ Total listings found: {len(posts)}")

# For storing unique vehicles
vehicles = set()

# Open each post, scrape info
for idx, post in enumerate(posts):
    try:
        driver.execute_script("arguments[0].scrollIntoView();", post)
        time.sleep(2)
        post.click()
        time.sleep(3)

        body_text = driver.find_element(By.TAG_NAME, 'body').text

        # Extract important details to make it unique
        lines = body_text.split('\n')
        price = next((line for line in lines if 'CA$' in line), "No Price")
        year_make_model = next((line for line in lines if any(char.isdigit() for char in line) and any(char.isalpha() for char in line)), "No Model")
        location = next((line for line in lines if 'NS' in line or 'NB' in line), "No Location")

        unique_key = f"{price} | {year_make_model} | {location}"
        vehicles.add(unique_key)

        print(f"✅ Scraped post {idx + 1}: {unique_key}")

        driver.back()
        time.sleep(3)

        posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/marketplace/item/")]')

    except Exception as e:
        print(f"⚠️ Error at post {idx+1}: {e}")
        driver.back()
        time.sleep(3)
        posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/marketplace/item/")]')
        continue

# Save all vehicles into an Excel
df = pd.DataFrame(list(vehicles), columns=["Vehicle Information"])
df.to_excel("marketplace_vehicles.xlsx", index=False)

print("✅ All vehicle data saved to 'marketplace_vehicles.xlsx'.")

driver.quit()