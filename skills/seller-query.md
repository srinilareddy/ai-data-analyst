# Seller Query Patterns

## Top sellers by revenue
```sql
SELECT i.seller_id,
       ROUND(SUM(i.price)::NUMERIC, 2) AS sales,
       COUNT(DISTINCT o.order_id) AS orders
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1 ORDER BY sales DESC LIMIT 10;
```

## Sellers by state
```sql
SELECT s.seller_state, COUNT(*) AS sellers
FROM sellers s GROUP BY 1 ORDER BY sellers DESC;
```

## Seller late delivery rate
```sql
SELECT i.seller_id,
  ROUND(100.0 * SUM(CASE WHEN
    o.order_delivered_customer_date::TIMESTAMP >
    o.order_estimated_delivery_date::TIMESTAMP
    THEN 1 ELSE 0 END)/COUNT(*),2) AS late_pct,
  COUNT(*) AS delivered
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1 HAVING COUNT(*) > 50
ORDER BY late_pct DESC;
```
