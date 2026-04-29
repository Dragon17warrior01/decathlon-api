# 🏪 Decathlon Product Analytics API

A FastAPI-based analytics project that extracts, processes, and analyzes product data from Decathlon India.  
This project demonstrates an **end-to-end data pipeline** including web scraping, data processing, SQL storage, analytics, REST API development, and BI reporting.

---

## 🚀 Features

- 🕷️ Web scraping pipeline to collect Decathlon product data
- 🧹 Data cleaning and transformation using Pandas
- 🗄️ SQL data storage and querying via Supabase (PostgreSQL)
- 📊 Analytical insights on product pricing and categories
- ⚡ FastAPI endpoints for accessing analytics results
- 📈 Visualizations generated from processed data
- 📉 Interactive Power BI dashboard for business insights

---

## 🌐 Live Demo

| Resource | Link |
|----------|------|
| 📄 API Docs (Swagger) | https://decathlon-api-63fi.onrender.com/docs |
| 🔗 Base URL | https://decathlon-api-63fi.onrender.com |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/products` | Get all scraped products |
| GET | `/analytics` | Get analytics summary |
| GET | `/plots` | View generated visualizations |

---

## 📊 Power BI Dashboard

An interactive **Decathlon Brand & Product Analysis** dashboard built using data from the live API.

![Decathlon Power BI Dashboard](outputs/dashboard_screenshot.png)

> 🔗 **Dashboard Link (internal access):** [View on SharePoint](https://scoe365-my.sharepoint.com/:u:/g/personal/21-101055_scoe365_onmicrosoft_com/IQA3vCfBb0QSRL6REG4bMPjOASSECAHLJ7mDDP2vKggAEEo?e=I0aX3H)  
> ⚠️ *This link requires access to the college Microsoft 365 account. See the screenshot above for a preview.*

### 📌 Key Insights
- **QUECHUA** has the highest product count (34) among all 12 brands
- **Running Shoes** dominate with 53 products across 11 categories
- Majority of brands contribute a small share — top 4 brands cover ~85% of products
- Built with slicers for dynamic **Filter by Category** exploration

> 🛠️ Tools used: Power BI Desktop · Data source: Live REST API (`/products` endpoint)

---

## 🗄️ SQL & Database (Supabase)

Product data is stored and queried using **Supabase (PostgreSQL)** as the backend database.

### Schema

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT,
    category TEXT,
    price NUMERIC,
    url TEXT,
    scraped_at TIMESTAMP DEFAULT NOW()
);
```

### Sample Analytical Queries

> 📁 Full queries available in [`analytics/queries.sql`](analytics/queries.sql)

```sql
-- Average price by category
SELECT category, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;

-- Product count per brand
SELECT brand, COUNT(*) AS product_count
FROM products
GROUP BY brand
ORDER BY product_count DESC;

```

> 🛠️ Tools used: Supabase · PostgreSQL · `supabase-py` / `psycopg2`

---

## 🧱 Project Structure

```
decathlon-api/
├── api/              # FastAPI routes and app entry point
├── analytics/        # Analytics logic and calculations
│   └── queries.sql   # SQL queries for Supabase
├── scraping/         # Web scraping / ETL pipeline
├── data/             # Raw and processed data files
├── outputs/
│   ├── plots/        # Generated visualizations
│   └── dashboard_screenshot.png  # Power BI dashboard preview
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

### ▶️ Run the API Locally
```bash
uvicorn api.main:app --reload
```
Then open: http://localhost:8000/docs

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| FastAPI | REST API framework |
| Pandas | Data processing |
| Matplotlib / Seaborn | Data visualization |
| BeautifulSoup / Requests | Web scraping |
| Supabase (PostgreSQL) | SQL database & storage |
| Power BI | Business intelligence dashboard |
| Render | Cloud deployment |

---

## 👤 Author

**Dragon17warrior01**  
🔗 GitHub: [@Dragon17warrior01](https://github.com/Dragon17warrior01)  
💼 LinkedIn: [linkedin.com/in/prajaktaningole](https://www.linkedin.com/in/prajaktaningole)

---

## 📌 Note

This project was built as a portfolio project to demonstrate data engineering and API development skills. The scraping is done for educational purposes only.
