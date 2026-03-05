import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths (leave pricing plots where they are — no issue)
DATA_PATH = "data/decathlon_pdp_final.csv"
OUTPUT_DIR = "outputs/plots"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load CSV (read-only)
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Clean price column IN-MEMORY only
df["Selling_Price"] = (
    df["Selling_Price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# --------------------------------------------------
# 1. Top 10 Brands by Product Count
# --------------------------------------------------
plt.figure(figsize=(10, 5))
df["Brand"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Brands by Product Count")
plt.xlabel("Brand")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top_brands_by_count.png")
plt.close()

# --------------------------------------------------
# 2. Top 10 Brands by Average Selling Price
# --------------------------------------------------
plt.figure(figsize=(10, 5))
df.groupby("Brand")["Selling_Price"].mean().sort_values(ascending=False).head(10).plot(kind="bar")
plt.title("Top 10 Brands by Average Selling Price")
plt.xlabel("Brand")
plt.ylabel("Average Price (INR)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/avg_price_by_brand.png")
plt.close()

# --------------------------------------------------
# 3. Brand Dominance Across Categories
# --------------------------------------------------
top_brands = df["Brand"].value_counts().head(5).index
filtered_df = df[df["Brand"].isin(top_brands)]

pivot = pd.pivot_table(
    filtered_df,
    index="Category",
    columns="Brand",
    values="Product_Name",
    aggfunc="count"
)

pivot.plot(kind="bar", figsize=(12, 6))
plt.title("Brand Dominance Across Categories")
plt.xlabel("Category")
plt.ylabel("Product Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/brand_category_dominance.png")
plt.close()

print("✅ Brand–Category analysis completed. Plots saved.")
