import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# =====================================================
# CONFIG
# =====================================================
INPUT_CSV = "data/decathlon_product_urls.csv"
OUTPUT_CSV = "data/decathlon_pdp_clean.csv"
URL_COLUMN = "Product_URL"

# =====================================================
# SELENIUM SETUP (STABILITY MODE)
# =====================================================
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-features=VizDisplayCompositor")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# =====================================================
# HELPERS
# =====================================================
def clean_price(text):
    return int(
        text.replace("₹", "")
            .replace(",", "")
            .strip()
    )

# =====================================================
# PDP SCRAPER (CRASH-SAFE)
# =====================================================
def scrape_pdp(url):
    print(f"🔍 Scraping: {url}")
    driver.get(url)

    # 🔥 CRITICAL: allow React to fully re-render
    time.sleep(5)

    data = {
        "product_url": url,
        "product_id": None,
        "brand": None,
        "product_name": None,
        "mrp": None,
        "selling_price": None,
        "discount_amount": None,
        "discount_percent": None,
        "product_in_stock": False,
        "available_sizes": None,
        "unavailable_sizes": None,
        "available_colours": None,
        "unavailable_colours": None
    }

    # -------------------------------
    # Product name
    # -------------------------------
    data["product_name"] = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    ).text.strip()

    # -------------------------------
    # Brand (fallback-safe)
    # -------------------------------
    try:
        brand_el = driver.find_element(
            By.XPATH, "//*[contains(@data-testid,'brand')]"
        )
        data["brand"] = brand_el.text.strip().upper()
    except NoSuchElementException:
        data["brand"] = "UNKNOWN"

    # -------------------------------
    # Product ID
    # -------------------------------
    try:
        pid = driver.find_element(
            By.XPATH, "//*[contains(text(),'ID')]"
        ).text
        data["product_id"] = pid.replace("ID:", "").strip()
    except NoSuchElementException:
        data["product_id"] = None

    # -------------------------------
    # Selling price
    # -------------------------------
    selling_el = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(@data-testid,'price')]")
        )
    )
    data["selling_price"] = clean_price(selling_el.text)

    # -------------------------------
    # MRP
    # -------------------------------
    try:
        mrp_el = driver.find_element(
            By.XPATH, "//*[contains(text(),'MRP')]"
        )
        data["mrp"] = clean_price(mrp_el.text)
    except NoSuchElementException:
        data["mrp"] = data["selling_price"]

    # -------------------------------
    # Discount (computed only)
    # -------------------------------
    data["discount_amount"] = data["mrp"] - data["selling_price"]
    data["discount_percent"] = round(
        (data["discount_amount"] / data["mrp"]) * 100, 2
    ) if data["mrp"] else 0

    # -------------------------------
    # Product stock
    # -------------------------------
    try:
        add_to_cart = driver.find_element(
            By.XPATH, "//button[contains(.,'Add')]"
        )
        data["product_in_stock"] = add_to_cart.is_enabled()
    except NoSuchElementException:
        data["product_in_stock"] = False

    # -------------------------------
    # Sizes
    # -------------------------------
    available_sizes = []
    unavailable_sizes = []

    for btn in driver.find_elements(
        By.XPATH, "//button[contains(@class,'size')]"
    ):
        size = btn.text.strip()
        if not size:
            continue
        if btn.get_attribute("disabled"):
            unavailable_sizes.append(size)
        else:
            available_sizes.append(size)

    data["available_sizes"] = ",".join(available_sizes) if available_sizes else None
    data["unavailable_sizes"] = ",".join(unavailable_sizes) if unavailable_sizes else None

    # -------------------------------
    # Colours
    # -------------------------------
    available_colours = []
    unavailable_colours = []

    for btn in driver.find_elements(
        By.XPATH, "//button[contains(@class,'color')]"
    ):
        label = btn.get_attribute("aria-label")
        if not label:
            continue
        if btn.get_attribute("disabled"):
            unavailable_colours.append(label)
        else:
            available_colours.append(label)

    data["available_colours"] = ",".join(available_colours) if available_colours else None
    data["unavailable_colours"] = ",".join(unavailable_colours) if unavailable_colours else None

    # -------------------------------
    # Validation
    # -------------------------------
    if data["selling_price"] > data["mrp"]:
        raise ValueError("Invalid price logic")

    return data

# =====================================================
# MAIN (RESUME-SAFE)
# =====================================================
if __name__ == "__main__":
    urls_df = pd.read_csv(INPUT_CSV)

    # ⛔ Skip first URL (known unstable)
    urls = urls_df[URL_COLUMN].dropna().unique().tolist()[1:]

    if os.path.exists(OUTPUT_CSV):
        existing = pd.read_csv(OUTPUT_CSV)
        done_urls = set(existing["product_url"].dropna().tolist())
        print(f"🔁 Resuming. Already scraped: {len(done_urls)}")
    else:
        done_urls = set()
        print("🆕 Starting fresh scrape")

    for url in urls:
        if url in done_urls:
            continue

        try:
            row = scrape_pdp(url)
            pd.DataFrame([row]).to_csv(
                OUTPUT_CSV,
                mode="a",
                header=not os.path.exists(OUTPUT_CSV),
                index=False
            )
            time.sleep(3)

        except Exception as e:
            print(f"❌ FAILED: {url} -> {e}")

    driver.quit()
    print("✅ PDP scrape finished (stable & resume-safe)")
