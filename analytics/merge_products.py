import pandas as pd

men = pd.read_csv("data/final_decathlon_products.csv")
women_kids = pd.read_csv("data/final_decathlon_products_extended.csv")

final = pd.concat([men, women_kids], ignore_index=True)

final.to_csv("data/decathlon_all_products.csv", index=False)

print("Merge complete ✅")
print("Men products:", len(men))
print("Women & Kids products:", len(women_kids))
print("Total products:", len(final))
