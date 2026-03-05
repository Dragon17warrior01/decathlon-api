import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import time
import random
import os

INPUT_CSV = "data/decathlon_urls_clean.csv"
OUTPUT_CSV = "data/decathlon_pdp_raw.csv"


async def scrape_product(page, url):
    return {
        "Product_URL": url,
        "Product_Name": None,
        "Category": None,
        "Rating": None,
        "Description": None,
    }


async def extract_fields(page, data):
    try:
        data["Product_Name"] = await page.locator("h1").first.inner_text()
    except:
        pass

    try:
        crumbs = await page.locator("nav a").all_inner_texts()
        data["Category"] = " > ".join(crumbs[:3])
    except:
        pass

    try:
        data["Rating"] = await page.locator('[data-testid="rating"]').inner_text()
    except:
        pass

    try:
        data["Description"] = await page.locator('[data-testid="product-description"]').inner_text()
    except:
        pass

    return data


async def main():
    df_urls = pd.read_csv(INPUT_CSV)
    urls = df_urls["Product_URL"].dropna().tolist()

    file_exists = os.path.exists(OUTPUT_CSV)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i, url in enumerate(urls, start=1):
            print(f"[{i}/{len(urls)}] Scraping:", url)

            data = {
                "Product_URL": url,
                "Product_Name": None,
                "Category": None,
                "Rating": None,
                "Description": None,
            }

            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")
                data = await extract_fields(page, data)
            except Exception as e:
                print("Error:", e)

            # Save immediately (append mode)
            pd.DataFrame([data]).to_csv(
                OUTPUT_CSV,
                mode="a",
                header=not file_exists,
                index=False
            )
            file_exists = True

            time.sleep(random.uniform(1.2, 2.5))

        await browser.close()

    print("✅ PDP scraping completed (incremental save).")


if __name__ == "__main__":
    asyncio.run(main())
