import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
DATA_PATH = DATA_PATH = "data/decathlon_pdp_final.csv"
OUTPUT_DIR = "../outputs/plots"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load CSV (read-only)
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Clean numeric columns IN-MEMORY only
df["Selling_Price"] = (
    df["Selling_Price"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["MRP"] = (
    df["MRP"]
    .astype(str)
    .str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# -----------------------------
# 1. Price Distribution
# -----------------------------
plt.figure()
df["Selling_Price"].dropna().hist(bins=30)
plt.title("Price Distribution (Men)")
plt.xlabel("Selling Price (INR)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/price_distribution.png")
plt.close()

# -----------------------------
# 2. Avg Price per Category
# -----------------------------
plt.figure(figsize=(10, 5))
df.groupby("Category")["Selling_Price"].mean().sort_values(ascending=False).plot(kind="bar")
plt.title("Average Selling Price per Category")
plt.xlabel("Category")
plt.ylabel("Average Price (INR)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/avg_price_per_category.png")
plt.close()

# -----------------------------
# 3. Avg Discount % per Category
# -----------------------------
plt.figure(figsize=(10, 5))
df.groupby("Category")["Discount_Percent"].mean().sort_values(ascending=False).plot(kind="bar")
plt.title("Average Discount Percentage per Category")
plt.xlabel("Category")
plt.ylabel("Discount %")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/discount_by_category.png")
plt.close()

print("✅ Pricing analysis completed. Plots saved.")
