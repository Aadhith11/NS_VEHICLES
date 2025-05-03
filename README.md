# NS_VEHICLES

## 📌 Project Overview
NS_VEHICLES is an automated scraping and data collection platform for Facebook Marketplace vehicle listings in Nova Scotia. It collects posts with details like price, model, year, location, seller name, and more. The system dynamically stores these entries in a structured format and aims for daily updates.

---

## 🔧 Tools & Tech Stack
- **Python 3.13**
- **Selenium** – browser automation
- **PyAutoGUI** – screen interaction, prevents sleep
- **Pytesseract + OCR** – for image-to-text extraction
- **Pandas** – for data storage and Excel output
- **Tesseract** – OCR backend
- **Chrome Debugging Protocol** – for connecting live Chrome
- **VS Code & GitHub Copilot** – development

---

## 🧩 Project Structure
```bash
NS_VEHICLES/
├── cookie_script.py             # Authenticates Facebook session with cookies
├── text_script.py               # Scrapes text content from vehicle posts
├── vision_script.py            # Uses OCR to extract text from screenshots
├── parse_vehicle_data.py       # Converts raw scraped text into structured data
├── Results/                    # Daily result folders (text + Excel)
│   ├── Results 26th/
│   ├── Results 27th/
│   └── result28/
├── marketplace_full_posts.txt  # All posts from text_script
├── optimized_final_posts.txt   # Final unique text from OCR
├── final_unique_posts.txt      # Filtered cleaned posts
├── marketplace_vehicles.xlsx   # Final structured data in Excel
├── vehicles.csv / .json        # Data formats
├── README.md                   # Project documentation