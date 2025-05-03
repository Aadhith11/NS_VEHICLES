# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyautogui  # To simulate mouse movement to prevent screen sleep

# Setup Selenium to connect to existing Chrome instance with debugging mode
options = Options()
options.debugger_address = "localhost:9222"  # Chrome started with --remote-debugging-port=9222

# Specify path to your chromedriver
path = '/Users/aadhithkumaresan/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)

# Check that the user is on Facebook Marketplace
current_url = driver.current_url
if not current_url.startswith('https://www.facebook.com/marketplace/'):
    print(f"❌ Not at Facebook Marketplace, exiting.")
    driver.quit()
    exit()

print("✅ Correct page detected. Starting scrape...")

# Step 1: Scroll down the page multiple times to load more posts
for _ in range(50):  # Scroll 50 times
    try:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # Scroll to bottom
        time.sleep(4)  # Wait for new posts to load

        # Move the mouse slightly to prevent screen from sleeping
        pyautogui.moveRel(10, 0, duration=0.2)  # Move mouse 10 pixels right
        pyautogui.moveRel(-10, 0, duration=0.2) # Move mouse 10 pixels left

    except Exception:
        # If any error during scroll, skip and continue
        continue

# Step 2: After scrolling, collect all the post elements
listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/marketplace/item/")]')
print(f"✅ Total listings found: {len(listings)}")

# Step 3: Open a text file to save the post content
with open('marketplace_full_posts.txt', 'w', encoding='utf-8') as file:

    # Step 4: Loop through each post one by one
    for index, listing in enumerate(listings):
        try:
            # Scroll the post into view to ensure it is clickable
            driver.execute_script("arguments[0].scrollIntoView();", listing)
            time.sleep(2)

            # Click the listing to open the post
            listing.click()
            time.sleep(4)  # Wait for the post to fully open

            try:
                # Extract all visible text from the post
                post_content = driver.find_element(By.TAG_NAME, 'body').text
            except:
                # If unable to extract text, store a message
                post_content = "Unable to extract post."

            # Write the post content into the file
            file.write(post_content)
            file.write("\n\n" + "-"*50 + "\n\n")  # Add a separator after each post

            print(f"✅ Saved post {index + 1}/{len(listings)}")

            # After saving, go back to the listing page
            driver.back()
            time.sleep(3)

            # Refresh listings elements because DOM may have changed
            listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/marketplace/item/")]')

        except Exception as e:
            # Handle errors without stopping the whole script
            print(f"⚠️ Error at post {index + 1}: {e}")
            try:
                driver.back()
                time.sleep(3)
                # Refresh listings after going back
                listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/marketplace/item/")]')
            except:
                continue

# Step 5: After scraping all posts, leave the browser open
print("✅ All posts saved into 'marketplace_full_posts.txt'")