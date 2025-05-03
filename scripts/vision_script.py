from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytesseract
import pyautogui
from PIL import ImageGrab
import os

# Setup Tesseract path
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Setup Chrome Debugger connection
options = Options()
options.debugger_address = "localhost:9222"

path = '/Users/aadhithkumaresan/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)

# Validate page
if not driver.current_url.startswith('https://www.facebook.com/marketplace/'):
    print(f"❌ Not at Facebook Marketplace. Exiting.")
    driver.quit()
    exit()

print("✅ Connected to Facebook Marketplace.")

# Variables
seen_posts = set()
move_cursor_toggle = True
scroll_pause_time = 1.5
same_scrolls = 0
max_same_scrolls = 3

# Function to capture **only listing area**
def capture_listing_area():
    screen = pyautogui.screenshot()
    width, height = screen.size
    # Crop middle vertical section where posts usually are
    crop_area = (width * 0.1, height * 0.2, width * 0.9, height * 0.85)
    cropped_screen = screen.crop(crop_area)
    return pytesseract.image_to_string(cropped_screen)

# Get initial scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

scroll_count = 0

while True:
    scroll_count += 1

    # Scroll down
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause_time)

    # Move mouse slightly every 5 scrolls
    if scroll_count % 5 == 0:
        pyautogui.move(5, 0)
        pyautogui.move(-5, 0)

    # OCR detection
    extracted_text = capture_listing_area()
    lines = extracted_text.splitlines()
    
    new_posts = 0
    for line in lines:
        if 'CA$' in line and line not in seen_posts:
            seen_posts.add(line)
            new_posts += 1

    # Scroll height check
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_posts == 0 and new_height == last_height:
        same_scrolls += 1
        print(f"⚡ No new posts detected. Same height count: {same_scrolls}")
    else:
        same_scrolls = 0
        print(f"✅ Scroll {scroll_count}: Found {new_posts} new unique posts. Running total: {len(seen_posts)}")

    last_height = new_height

    if same_scrolls >= max_same_scrolls:
        print("✅ No new posts detected after multiple scrolls. Finishing up.")
        break

# Save results
with open('optimized_final_posts.txt', 'w', encoding='utf-8') as f:
    for post in seen_posts:
        f.write(post + '\n')

driver.quit()
print(f"✅ Total unique posts captured: {len(seen_posts)}")