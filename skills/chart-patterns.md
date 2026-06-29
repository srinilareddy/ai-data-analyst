# Chart Patterns

Standard chart types and when to use each. Generate clean matplotlib code
that saves a PNG to the charts/ folder.

## Setup for every chart
```python
import matplotlib
matplotlib.use('Agg')  # no display needed, save to file
import matplotlib.pyplot as plt
import os
os.makedirs('charts', exist_ok=True)
```

## Line chart — trends over time
Use for: revenue by month, orders over time.
```python
plt.figure(figsize=(10,5))
plt.plot(months, revenue, marker='o')
plt.title('Monthly Revenue')
plt.xlabel('Month'); plt.ylabel('Revenue (R$)')
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig('charts/monthly_revenue.png', dpi=120)
```

## Bar chart — comparing categories
Use for: revenue by category, orders by state.
```python
plt.figure(figsize=(10,5))
plt.barh(categories, values)   # horizontal = easier to read labels
plt.title('Revenue by Category')
plt.tight_layout()
plt.savefig('charts/revenue_by_category.png', dpi=120)
```

## Grouped/stacked bar — parts of a whole over time
Use for: new vs repeat customers by month.

## Choosing a chart
- Change over time -> line
- Comparing items -> horizontal bar
- Composition -> stacked bar or pie (pie only for 2-5 slices)
- Relationship between two numbers -> scatter

## Rules
- Always save to charts/ as PNG, never just show
- Always label title, axes, and units
- Keep it clean — no chartjunk, readable fonts
- Sort bars by value so the ranking is obvious