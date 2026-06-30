# Customer Query Patterns

## Repeat purchase rate
(see kpi-definitions.md — uses customer_unique_id)

## New vs repeat customers by month
```sql
WITH first_order AS (
  SELECT c.customer_unique_id,
         MIN(o.order_purchase_timestamp::TIMESTAMP) AS first_dt
  FROM orders o JOIN customers c ON o.customer_id = c.customer_id
  WHERE o.order_status = 'delivered'
  GROUP BY 1)
SELECT DATE_TRUNC('month', o.order_purchase_timestamp::TIMESTAMP) AS month,
  COUNT(*) FILTER (WHERE DATE_TRUNC('month', o.order_purchase_timestamp::TIMESTAMP)
    = DATE_TRUNC('month', f.first_dt)) AS new_customers,
  COUNT(*) FILTER (WHERE DATE_TRUNC('month', o.order_purchase_timestamp::TIMESTAMP)
    > DATE_TRUNC('month', f.first_dt)) AS repeat_customers
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN first_order f ON c.customer_unique_id = f.customer_unique_id
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY 1;
```

## Customers by state
```sql
SELECT c.customer_state,
       COUNT(DISTINCT c.customer_unique_id) AS customers
FROM customers c
GROUP BY 1 ORDER BY customers DESC;
```