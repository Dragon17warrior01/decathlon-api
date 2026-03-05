import pandas as pd

df = pd.read_csv("data/decathlon_all_products_text_clean.csv")

def split_rating(x):
    if pd.isna(x) or "|" not in str(x):
        return pd.Series([None, None])
    r, c = x.split("|")
    return pd.Series([float(r.strip()), c.strip()])

df[["Rating", "Review_Count"]] = df["Rating"].apply(split_rating)

df.to_csv("data/decathlon_all_products_clean.csv", index=False)
print("Ratings fixed ✅")
