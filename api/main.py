from fastapi import FastAPI
from fastapi import FastAPI
from api.supabase_client import supabase

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Decathlon Product API running"}

@app.get("/products")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data