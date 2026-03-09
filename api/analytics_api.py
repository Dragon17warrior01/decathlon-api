from fastapi import APIRouter
import pandas as pd
from api.supabase_client import supabase

router = APIRouter()

# BRAND DISTRIBUTION
@router.get("/analytics/brands")
def brand_distribution():
    response = supabase.table("products").select("Brand").execute()
    df = pd.DataFrame(response.data)

    return df["Brand"].value_counts().to_dict()


# CATEGORY DISTRIBUTION
@router.get("/analytics/categories")
def category_distribution():
    response = supabase.table("products").select("Category").execute()
    df = pd.DataFrame(response.data)

    return df["Category"].value_counts().to_dict()


# PRICE STATS
@router.get("/analytics/prices")
def price_statistics():
    response = supabase.table("products").select("Selling_Price").execute()
    df = pd.DataFrame(response.data)

    return {
        "avg_price": float(df["Selling_Price"].mean()),
        "max_price": float(df["Selling_Price"].max()),
        "min_price": float(df["Selling_Price"].min())
    }


# DISCOUNT STATS
@router.get("/analytics/discounts")
def discount_statistics():
    response = supabase.table("products").select("Discount_Percent").execute()
    df = pd.DataFrame(response.data)

    return {
        "avg_discount": float(df["Discount_Percent"].mean()),
        "max_discount": float(df["Discount_Percent"].max()),
        "min_discount": float(df["Discount_Percent"].min())
    }