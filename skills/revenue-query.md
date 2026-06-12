# Revenue Query Patterns

Reusable SQL patterns for revenue analysis. Revenue always comes from
order_items.price, filtered to delivered orders.

## Total revenue
```sql
SELECT ROUND(SUM(i.price)::NUMERIC, 2) AS revenue
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered';
```

## Revenue by month
```sql
SELECT DATE_TRUNC('month', o.order_purchase_timestamp::TIMESTAMP) AS month,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(i.price)::NUMERIC, 2) AS revenue
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;
```

## Revenue by product category (English)
```sql
SELECT t.product_category_name_english AS category,
       ROUND(SUM(i.price)::NUMERIC, 2) AS revenue,
       COUNT(DISTINCT o.order_id) AS orders
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
JOIN products p ON i.product_id = p.product_id
JOIN category_translation t
     ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY revenue DESC;
```

## Revenue by customer state
```sql
SELECT c.customer_state,
       ROUND(SUM(i.price)::NUMERIC, 2) AS revenue,
       COUNT(DISTINCT o.order_id) AS orders
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY revenue DESC;
```

## Month-over-month revenue growth
```sql
WITH m AS (
  SELECT DATE_TRUNC('month', o.order_purchase_timestamp::TIMESTAMP) AS mo,
         SUM(i.price) AS rev
  FROM orders o
  JOIN order_items i ON o.order_id = i.order_id
  WHERE o.order_status = 'delivered'
  GROUP BY 1)
SELECT mo,
       ROUND(rev::NUMERIC, 2) AS revenue,
       ROUND(100.0 * (rev - LAG(rev) OVER (ORDER BY mo))
             / LAG(rev) OVER (ORDER BY mo), 2) AS mom_growth_pct
FROM m
ORDER BY mo;
```

## Notes
- Always use order_items.price, never payments.payment_value
- Always filter order_status = 'delivered'
- Cast timestamps with ::TIMESTAMP before DATE_TRUNC