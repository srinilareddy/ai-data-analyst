import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine('postgresql://localhost/olist_db')

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(script_dir, 'dataset')
os.chdir(dataset_dir)

files = {
    'orders': 'olist_orders_dataset.csv',
    'customers': 'olist_customers_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'payments': 'olist_order_payments_dataset.csv',
    'reviews': 'olist_order_reviews_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv',
    'category_translation': 'product_category_name_translation.csv'
}

for table, file in files.items():
    if os.path.exists(file):
        df = pd.read_csv(file)
        df.to_sql(table, engine, if_exists='replace', index=False)
        print(f"✓ Loaded {table} — {len(df)} rows")
    else:
        print(f"✗ File not found: {file}")

