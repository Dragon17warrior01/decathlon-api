import pandas as pd

# Load both URL files
df1 = pd.read_csv("data/decathlon_product_urls.csv")
df2 = pd.read_csv("data/decathlon_product_urls_extended.csv")

# Combine both
df = pd.concat([df1, df2], ignore_index=True)

print("Rows before deduplication:", len(df))

# Remove exact duplicate URLs (keep all colors)
df_clean = df.drop_duplicates(subset=["Product_URL"])

print("Rows after deduplication:", len(df_clean))

# Save final clean file
df_clean.to_csv("data/decathlon_urls_clean.csv", index=False)
