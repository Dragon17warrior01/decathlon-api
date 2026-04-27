# Decathlon Product Analytics API

A FastAPI-based analytics project that extracts, processes, and analyzes product data from Decathlon. This project demonstrates end-to-end data pipeline skills including web scraping, data processing, analytics, and API development.

---

## 🚀 Features

* Web scraping pipeline to collect product data
* Data cleaning and transformation
* Analytical insights on product pricing and categories
* FastAPI endpoints for accessing analytics
* Visualizations generated from processed data

---

## 📊 API Endpoints

| Endpoint     | Description                   |
| ------------ | ----------------------------- |
| `/`          | Health check                  |
| `/products`  | Get all products              |
| `/analytics` | Get analytics summary         |
| `/plots`     | View generated visualizations |

---

## 🧱 Project Structure

```
decathlon-api/
├── api/              # FastAPI routes and endpoints
├── analytics/        # Analytics logic and calculations  
├── scraping/         # ETL pipeline and web scraping
├── data/             # Raw and processed data files
├── outputs/plots/    # Generated visualisations
├── requirements.txt  # Python dependencies
└── start.sh          # Startup script
```

---

## ⚙️ Installation

```
git clone https://github.com/your-username/decathlon-api.git
cd decathlon-api
pip install -r requirements.txt
```

---

## ▶️ Run the API

```
uvicorn api.main:app --reload
```

---

## 🌐 Live Demo

API Docs: https://decathlon-api-63fi.onrender.com/docs  
Base URL: https://decathlon-api-63fi.onrender.com/

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Pandas
* Matplotlib / Seaborn
* Web Scraping

---

## 👤 Author

* LinkedIn: https://linkedin.com/in/your-profile
* GitHub: https://github.com/your-username
