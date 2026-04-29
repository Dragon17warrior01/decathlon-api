-- ============================================
-- Decathlon Product Analytics - SQL Queries
-- Database: Supabase (PostgreSQL)
-- ============================================

-- 1. Total product count
SELECT COUNT(*) AS total_products FROM products;

-- 2. Product count per brand
SELECT brand, COUNT(*) AS product_count
FROM products
GROUP BY brand
ORDER BY product_count DESC;

-- 3. Average price by category
SELECT category, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;

-- 4. Top 5 most expensive products
SELECT name, brand, category, price
FROM products
ORDER BY price DESC
LIMIT 5;

-- 5. Most affordable products per category
SELECT DISTINCT ON (category)
    category, name, brand, price
FROM products
ORDER BY category, price ASC;

-- 6. Brand market share (% of total products)
SELECT brand,
       COUNT(*) AS product_count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_percentage
FROM products
GROUP BY brand
ORDER BY share_percentage DESC;

-- 7. Price range (min, max, avg) per brand
SELECT brand,
       MIN(price) AS min_price,
       MAX(price) AS max_price,
       ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY brand
ORDER BY avg_price DESC;
