## 📌 Project Overview

NS_VEHICLES is an automated scraping and data collection platform for Facebook Marketplace vehicle listings in Nova Scotia. It collects posts with details like:

- Price (CAD)
- Year, Make, Model
- Location
- Seller Name
- Estimated Post Date

The system dynamically stores these entries in a structured format and aims for daily updates.

---

## ⚙️ Tools & Tech Stack

- **🧠 Python 3.13** — core language
- **🕸 Selenium** — browser automation
- **🖱 PyAutoGUI** — screen interaction, prevents sleep
- **🔍 Pytesseract (OCR)** — image-to-text extraction
- **📦 Pandas** — data storage and Excel/CSV output
- **🧠 Tesseract** — OCR backend (via Homebrew on macOS)
- **🧩 Chrome Debugging Protocol** — for live browser connection
- **🧑‍💻 VS Code + GitHub Copilot** — for development

---

## 🧩 Real-World Use Case

Facebook Marketplace currently displays only **relative timestamps** such as:
- "1 hour ago", "1 day ago", "2 weeks ago", "4 weeks ago"

This makes it difficult to:
- Know the **exact date a vehicle was posted**.
- Track how long listings remain online.
- Validate claims regarding vehicle purchase dates and prices.

**NS_VEHICLES solves this by creating a daily record** of all listings, giving each entry an estimated post date and saving it to a structured database.

This is critical for:
- 📅 Building a historical log of vehicle listings.
- 🧾 Preventing **fraudulent tax claims**, e.g., falsely reporting that a Porsche worth $80,000 was bought for $150.
- 📑 Supporting audit processes with timestamped evidence.
- 🔍 Market research and pricing trend analysis.

---

## 📂 Project Structure

```bash
NS_VEHICLES/
├── scripts/
│   ├── cookie_script.py         # Authenticates Facebook session with cookies
│   ├── text_script.py           # Scrapes text content from vehicle posts
│   ├── vision_script.py         # Uses OCR to extract text from screenshots
│   └── parse_vehicle_data.py    # Parses and organizes vehicle data
├── data/
│   ├── marketplace_vehicles.xlsx
│   ├── vehicles.csv
│   └── vehicles.json
├── Results.py/                  # Dated folders storing scrape sessions
├── README.md

## 🔐 Cookie Injection Required

This script is useful when login automation is restricted or blocked by CAPTCHA, as it uses manual cookie injection to preserve the session.

Chrome to be launched👇
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/ChromeProfile"