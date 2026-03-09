from fastapi import FastAPI
from api.supabase_client import supabase
from api.analytics_api import router as analytics_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Decathlon Product API running"}

@app.get("/products")
def get_products():
    response = supabase.table("products").select("*").execute()
    return response.data

# ADD THIS LINE
app.include_router(analytics_router)