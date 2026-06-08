# KPI Definitions — Olist E-commerce

## Revenue
Total money earned from delivered orders.
Use order_items.price, NOT payments.payment_value.

```sql
SELECT SUM(i.price) as revenue
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
```

## Average Order Value (AOV)
Total Revenue / Total Delivered Orders.

```sql
SELECT ROUND(SUM(i.price) / COUNT(DISTINCT o.order_id), 2) as aov
FROM order_items i
JOIN orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
```

## Order Fulfillment Rate
(Delivered Orders / Total Orders) × 100.

```sql
SELECT ROUND(
  100.0 * SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END)
  / COUNT(*), 2
) as fulfillment_rate_pct
FROM orders
```

## Late Delivery Rate
Orders delivered after the estimated date, as a percentage.

```sql
SELECT ROUND(
  100.0 * SUM(
    CASE WHEN order_delivered_customer_date::TIMESTAMP
              > order_estimated_delivery_date::TIMESTAMP
         THEN 1 ELSE 0 END
  ) / COUNT(*), 2
) as late_delivery_rate_pct
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
```

## Average Review Score
Average customer rating (1-5 scale).

```sql
SELECT ROUND(AVG(review_score::NUMERIC), 2) as avg_review_score
FROM reviews
```

## Repeat Purchase Rate
Percentage of customers who placed more than one order.

```sql
WITH customer_orders AS (
  SELECT customer_unique_id, COUNT(*) as order_count
  FROM orders o
  JOIN customers c ON o.customer_id = c.customer_id
  GROUP BY customer_unique_id
)
SELECT ROUND(
  100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)
  / COUNT(*), 2
) as repeat_purchase_rate_pct
FROM customer_orders
```