from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
import os

# =========================
# CONFIG
# =========================
INPUT_FILE = "data/decathlon_product_urls_extended.csv"
OUTPUT_FILE = "data/final_decathlon_products_extended.csv"
WAIT_TIME = 5

# =========================
# LOAD URLS
# =========================
df_urls = pd.read_csv(INPUT_FILE)

products = []
scraped_urls = set()

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

# =========================
# SAFE HELPERS
# =========================
def safe_text(by, value):
    try:
        return driver.find_element(by, value).text.strip()
    except:
        return ""

def safe_elements(by, value):
    try:
        return driver.find_elements(by, value)
    except:
        return []

def save_checkpoint():
    pd.DataFrame(products).to_csv(OUTPUT_FILE, index=False)

# =========================
# SCRAPE LOOP (ALL 186)
# =========================
for idx, row in df_urls.iterrows():
    url = row["Product_URL"]
    category = row["Category"]

    if url in scraped_urls:
        continue

    print(f"Scraping {idx + 1}/{len(df_urls)} → {url}")

    try:
        driver.get(url)
        time.sleep(WAIT_TIME)

        page_source = driver.page_source.lower()

        # ---------- PRODUCT NAME ----------
        product_name = safe_text(By.TAG_NAME, "h1")
        if not product_name:
            product_name = "Not Available"

        # ---------- BRAND (FALLBACK) ----------
        brand = safe_text(By.XPATH, "//a[contains(@href,'/brand')]")
        if not brand and product_name != "Not Available":
            brand = product_name.split()[0]
        if not brand:
            brand = "Not Available"

        # ---------- PRICES (ROBUST) ----------
        prices = re.findall(r"₹\s?[\d,]+", driver.page_source)
        prices = [int(p.replace("₹", "").replace(",", "").strip()) for p in prices]
        prices = sorted(set(prices))

        if len(prices) >= 2:
            discounted_price = f"₹{prices[0]}"
            original_price = f"₹{prices[-1]}"
        elif len(prices) == 1:
            discounted_price = original_price = f"₹{prices[0]}"
        else:
            discounted_price = original_price = "Not Available"

        # ---------- RATING ----------
        rating = safe_text(By.XPATH, "//span[contains(@class,'rating')]")
        rating = rating if rating else "Not Available"

        # ---------- REVIEW COUNT ----------
        review_count = safe_text(By.XPATH, "//span[contains(@class,'review')]")
        review_count = review_count if review_count else "Not Available"

        # ---------- AVAILABILITY ----------
        if "out of stock" in page_source or "currently unavailable" in page_source:
            availability = "Out of Stock"
        else:
            availability = "In Stock"

        # ---------- COLORS ----------
        colors = [
            c.get_attribute("aria-label")
            for c in safe_elements(By.XPATH, "//button[contains(@class,'color')]")
            if c.get_attribute("aria-label")
        ]
        colors = ", ".join(set(colors)) if colors else "Not Available"

        # ---------- SIZES ----------
        sizes = [
            s.text.strip()
            for s in safe_elements(By.XPATH, "//button[contains(@class,'size')]")
            if s.text.strip()
        ]
        sizes = ", ".join(set(sizes)) if sizes else "Not Available"

        products.append({
            "Product_URL": url,
            "Product_Name": product_name,
            "Brand": brand,
            "Category": category,
            "Original_Price": original_price,
            "Discounted_Price": discounted_price,
            "Rating": rating,
            "Review_Count": review_count,
            "Availability": availability,
            "Colors": colors,
            "Sizes": sizes
        })

        scraped_urls.add(url)
        save_checkpoint()

    except Exception as e:
        print(f"⚠️ Failed on {url} → {e}")
        continue

# =========================
# CLEAN SHUTDOWN (IMPORTANT)
# =========================
driver.quit()

print("\n==============================")
print("STAGE 2.1 COMPLETE (REFINED)")
print(f"Saved {len(products)} products")
print(f"File: {OUTPUT_FILE}")
print("==============================")
