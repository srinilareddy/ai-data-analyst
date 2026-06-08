# KPI Analyst - Project Context
## Data Sources
- PostgreSQL: olist_db (read-only, never run UPDATE/DELETE/DROP)
- CSV files: located in /dataset/ folder

## Key Tables & Columns

### orders
order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date

### customers
customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state

### order_items
order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value

### payments
order_id, payment_sequential, payment_type, payment_installments, payment_value

### reviews
review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date,review_answer_timestamp

### products
product_id, product_category_name, product_name_lenght, product_description_lenght,   product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm

### sellers
seller_id, seller_zip_code_prefix, seller_city, seller_state

### category_translation
product_category_name, product_category_name_english

## Key Joins
- orders -> customers on customer_id
- orders -> order_items on order_id
- order_items → products on product_id
- order_items → sellers on seller_id
- orders → payments on order_id
- orders → reviews on order_id
- products → category_translation on product_category_name

## KPI Questions This System Should Answer
- What is total revenue by month?
- Which product categories generate the most revenue?
- What is the average order value?
- Which sellers have the highest sales?
- What is the average delivery time?
- Which states have the most orders?
- What is the average review score by category?
- How many orders were delivered late?
- What is the repeat purchase rate?

## Rules for All Agents
- Never mutate data — SELECT only
- Always filter by order_purchase_timestamp for date ranges
- Round currency to 2 decimal places
- Use UTC for all timestamps
- Order status values: delivered, shipped, canceled, unavailable,
  invoiced, processing, created, approved