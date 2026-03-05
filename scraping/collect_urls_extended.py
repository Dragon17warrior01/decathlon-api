from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import sys

# =========================
# CONFIG — WOMEN + KIDS
# =========================
BASE_URLS = {
    # WOMEN
    ("Ordinary", "Women"): "https://www.decathlon.in/c/women-sport-shoes-16993?inStock%5B0%5D=1",
    ("Sport Shoes", "Women"): "https://www.decathlon.in/c/women-sport-shoes-16993?gender_id_en%5B0%5D=WOMEN&nature_id_en%5B0%5D=Sport%20Shoes&inStock%5B0%5D=1",

    # KIDS
    ("Kids Footwear", "Girls"): "https://www.decathlon.in/c/kids-footwear-17038?gender_id_en%5B0%5D=GIRLS&inStock%5B0%5D=1",
    ("Kids Footwear", "Boys"): "https://www.decathlon.in/c/kids-footwear-17038?gender_id_en%5B0%5D=BOYS&inStock%5B0%5D=1",
}

MAX_PAGES = 10
OUTPUT_FILE = "data/decathlon_product_urls_extended.csv"

# =========================
# CHROME SETUP
# =========================
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Store (url, category, gender) tuples
product_urls = set()

def save_urls():
    if not product_urls:
        print("No URLs collected.")
        return

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Product_URL", "Category", "Gender"])
        for url, category, gender in sorted(product_urls):
            writer.writerow([url, category, gender])

    print("\n==============================")
    print(f"SAVED {len(product_urls)} UNIQUE PRODUCT URLS")
    print(f"File: {OUTPUT_FILE}")
    print("==============================")

try:
    print("Starting Decathlon Stage 1 (Women + Kids) URL collection...")

    for (category, gender), base_url in BASE_URLS.items():
        print(f"\n===== CATEGORY: {category} | GENDER: {gender} =====")

        for page in range(1, MAX_PAGES + 1):
            page_url = f"{base_url}&page={page}"
            print(f"Scraping page {page}")

            driver.get(page_url)
            time.sleep(6)  # allow JS to load products

            anchors = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")

            before = len(product_urls)

            for a in anchors:
                href = a.get_attribute("href")
                if href:
                    product_urls.add((href, category, gender))

            after = len(product_urls)
            print(f"Collected {after - before} new URLs (Total: {after})")

except KeyboardInterrupt:
    print("\n⚠️ Interrupted by user. Saving progress...")
    save_urls()
    driver.quit()
    sys.exit(0)

except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    save_urls()
    driver.quit()
    sys.exit(1)

finally:
    driver.quit()
    save_urls()
