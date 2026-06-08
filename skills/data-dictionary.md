# Data Dictionary — Olist Database

## Important Notes
- All timestamp columns are stored as TEXT — always cast with ::TIMESTAMP
- Currency is in Brazilian Reais (R$)
- Dataset covers Oct 2016 to Aug 2018
- customer_id ≠ customer_unique_id — one real customer can have many customer_ids
- CSV files live in the dataset/ folder

## orders
order_id (text, PK), customer_id (text, FK), order_status (text),
order_purchase_timestamp (text), order_approved_at (text),
order_delivered_carrier_date (text), order_delivered_customer_date (text),
order_estimated_delivery_date (text)

## customers
customer_id (text), customer_unique_id (text, true customer ID),
customer_zip_code_prefix (text), customer_city (text), customer_state (text)

## order_items
order_id (text), order_item_id (int), product_id (text), seller_id (text),
price (numeric — USE FOR REVENUE), freight_value (numeric)

## payments
order_id (text), payment_type (text), payment_installments (int),
payment_value (numeric — includes fees, avoid for revenue)

## reviews
order_id (text), review_score (text — cast to NUMERIC),
review_comment_title (text), review_comment_message (text),
review_creation_date (text)

## products
product_id (text), product_category_name (text — Portuguese),
product_weight_g, product_length_cm, product_height_cm, product_width_cm

## sellers
seller_id (text), seller_zip_code_prefix (text),
seller_city (text), seller_state (text)

## category_translation
product_category_name (text — join key), product_category_name_english (text)

## Common Gotchas
- Use customer_unique_id not customer_id for counting customers
- Cast review_score::NUMERIC before AVG
- Cast timestamps::TIMESTAMP before date math
- Revenue = order_items.price, never payments.payment_value
- Filter order_status = 'delivered' for business metrics