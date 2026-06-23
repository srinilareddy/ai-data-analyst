# Forecasting Patterns

Simple, defensible forecasting methods for revenue and order volume.
These are projections, not guarantees — always state assumptions.

## Method 1: Moving average
Smooths short-term noise to show the underlying level. Good for a stable
series. A 3-month moving average = average of the last 3 months.

Use when: the series is flat or slowly changing (like 2018 revenue).

## Method 2: Linear trend (least squares)
Fits a straight line through the historical points and extends it.
Captures a steady upward or downward direction.

Use when: there's a clear consistent trend.
Python:
```python
import numpy as np
# x = period numbers (0,1,2,...), y = revenue values
coeffs = np.polyfit(x, y, 1)      # degree 1 = straight line
slope, intercept = coeffs
next_x = len(y)
forecast = slope * next_x + intercept
```

## Method 3: Growth rate projection
Apply a recent average growth rate forward. If revenue grew 2% MoM on
average recently, project next month = last month x 1.02.

Use when: the series grows by a roughly constant percentage.

## Choosing a method
- Flat/noisy series -> moving average
- Steady straight-line change -> linear trend
- Constant % growth -> growth rate projection

## Always report with a forecast
- The method used and why
- The assumption it rests on
- A range, not just a point (e.g. "R$950K-R$1.05M") to show uncertainty
- A caveat: forecasts assume conditions stay similar; one-off events
  (Black Friday, stockouts) will break them

## Important caveats for this dataset
- Data ends August 2018 and the last months are partial/declining as
  delivery data tapers off — don't over-trust the final 1-2 points
- 2018 revenue was a plateau, so a flat forecast is more honest than
  projecting the explosive 2017 growth forward