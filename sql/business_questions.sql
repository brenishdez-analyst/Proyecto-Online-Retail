-- Proyecto Online Retail: consultas de negocio

-- 1. Tendencia mensual de ingresos, pedidos y ticket promedio
SELECT
    substr(invoice_date, 1, 7) AS month,
    ROUND(SUM(line_revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(line_revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM sales
GROUP BY month
ORDER BY month;

-- 2. Países con más ingresos fuera del mercado principal
SELECT
    country,
    ROUND(SUM(line_revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers
FROM sales
WHERE country <> 'United Kingdom'
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;

-- 3. Productos con mayor ingreso (excluye códigos sin descripción)
SELECT
    stock_code,
    description,
    ROUND(SUM(line_revenue), 2) AS revenue,
    SUM(quantity) AS units,
    COUNT(DISTINCT invoice_no) AS orders
FROM sales
WHERE description IS NOT NULL
  AND UPPER(stock_code) NOT IN ('POST', 'DOT', 'M', 'BANK CHARGES', 'AMAZONFEE', 'CRUK', 'D', 'S')
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 20;

-- 4. Clientes con mayor valor acumulado
SELECT
    customer_id,
    ROUND(SUM(line_revenue), 2) AS lifetime_revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(line_revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY lifetime_revenue DESC
LIMIT 20;

-- 5. Distribución de clientes por segmento RFM
SELECT
    segment,
    COUNT(*) AS customers,
    ROUND(SUM(monetary), 2) AS revenue,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 1) AS avg_orders
FROM customer_rfm
GROUP BY segment
ORDER BY revenue DESC;
