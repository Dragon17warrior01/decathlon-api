# 🏪 Decathlon Product Analytics API

A FastAPI-based analytics project that extracts, processes, and analyzes product data from Decathlon India.

This project demonstrates an end-to-end data pipeline including web scraping, data processing, analytics, and REST API development.

---

## 🚀 Features

* 🕷️ Web scraping pipeline to collect Decathlon product data
* 🧹 Data cleaning and transformation using Pandas
* 📊 Analytical insights on product pricing and categories
* ⚡ FastAPI endpoints for accessing analytics results
* 📈 Visualizations generated from processed data

---

## 🌐 Live Demo

* 📄 **API Docs (Swagger):** https://decathlon-api-63fi.onrender.com/docs
* 🔗 **Base URL:** https://decathlon-api-63fi.onrender.com

---

## 📡 API Endpoints

| Method | Endpoint   | Description                   |
| ------ | ---------- | ----------------------------- |
| GET    | /          | Health check                  |
| GET    | /products  | Get all scraped products      |
| GET    | /analytics | Get analytics summary         |
| GET    | /plots     | View generated visualizations |

---

## 🧱 Project Structure

```
decathlon-api/
├── api/              # FastAPI routes and app entry point
├── analytics/        # Analytics logic and calculations
├── scraping/         # Web scraping / ETL pipeline
├── data/             # Raw and processed data files
├── outputs/plots/    # Generated visualizations
├── requirements.txt  # Python dependencies
└── start.sh          # Startup script
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dragon17warrior01/decathlon-api.git
cd decathlon-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the API Locally

```bash
uvicorn api.main:app --reload
```

Then open your browser at:
http://localhost:8000/docs

---

## 🛠️ Tech Stack

| Tool                     | Purpose            |
| ------------------------ | ------------------ |
| Python                   | Core language      |
| FastAPI                  | REST API framework |
| Pandas                   | Data processing    |
| Matplotlib / Seaborn     | Data visualization |
| BeautifulSoup / Requests | Web scraping       |
| Render                   | Cloud deployment   |

---

## 👤 Author

**Dragon17warrior01**

* 🔗 GitHub: @Dragon17warrior01
* 💼 LinkedIn: https://www.linkedin.com/in/prajaktaningole

---

## 📌 Note

This project was built as a portfolio project to demonstrate data engineering and API development skills.
The scraping is done for educational purposes only.
