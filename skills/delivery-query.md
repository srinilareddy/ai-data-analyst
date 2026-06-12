# Delivery Query Patterns

Reusable SQL patterns for delivery performance analysis. A late order
is one where the customer received it after the estimated delivery date.

## Late delivery rate
```sql
SELECT ROUND(
  100.0 * SUM(CASE WHEN order_delivered_customer_date::TIMESTAMP
                        > order_estimated_delivery_date::TIMESTAMP
                   THEN 1 ELSE 0 END) / COUNT(*), 2
) AS late_delivery_rate_pct
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;
```

## Average delivery time in days
```sql
SELECT ROUND(AVG(
  order_delivered_customer_date::TIMESTAMP
  - order_purchase_timestamp::TIMESTAMP
)::NUMERIC, 1) AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;
```

## Average delivery time by customer state
```sql
SELECT c.customer_state,
       ROUND(AVG(
         o.order_delivered_customer_date::TIMESTAMP
         - o.order_purchase_timestamp::TIMESTAMP
       )::NUMERIC, 1) AS avg_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1
ORDER BY avg_days DESC;
```

## Late deliveries by product category
```sql
SELECT t.product_category_name_english AS category,
       ROUND(100.0 * SUM(CASE WHEN
         o.order_delivered_customer_date::TIMESTAMP
         > o.order_estimated_delivery_date::TIMESTAMP
         THEN 1 ELSE 0 END) / COUNT(*), 2) AS late_pct
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
JOIN products p ON i.product_id = p.product_id
JOIN category_translation t
     ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY 1
ORDER BY late_pct DESC;
```

## Review score vs delivery timeliness
```sql
SELECT CASE WHEN o.order_delivered_customer_date::TIMESTAMP
                 > o.order_estimated_delivery_date::TIMESTAMP
            THEN 'late' ELSE 'on_time' END AS delivery_status,
       ROUND(AVG(r.review_score::NUMERIC), 2) AS avg_review_score,
       COUNT(*) AS orders
FROM orders o
JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1;
```

## Notes
- Late = delivered_customer_date > estimated_delivery_date
- Always exclude NULL delivery dates from late calculations
- Date subtraction returns an interval — cast to NUMERIC for rounding