import pandas as pd

# =========================
# LOAD MERGED DATA
# =========================
df = pd.read_csv("data/decathlon_all_products.csv", encoding="utf-8")

# =========================
# TEXT CLEANER
# =========================
def clean_text(x):
    if pd.isna(x):
        return x
    return (
        str(x)
        .replace("â‚¹", "₹")
        .replace("â€™", "'")
        .replace("Menâ€™s", "Men's")
        .replace("â€“", "-")
        .replace("Â", "")
        .strip()
    )

# =========================
# APPLY CLEANING
# =========================
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# =========================
# SAVE CLEAN FILE
# =========================
OUTPUT_FILE = "data/decathlon_all_products_text_clean.csv"
df.to_csv(OUTPUT_FILE, index=False)

print("Text cleaned ✅")
print(f"File saved: {OUTPUT_FILE}")
print("Rows:", len(df))
