---
idea: 037-01_falling-market-wide-day-decline
brief: 037_wide-days-precede-decline-in-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a day in a falling market whose high-low range is wide -> adapted: a "wide" day is a regime of the regime detector (range of at least 2 usual swings, the common two-standard-deviation convention), and the forecast is graded by width inside it; the falling-market profile is added by code.
- Comparison: the range against the coin's 30-day standard deviation of daily returns -> kept: RangeInReturnStdComponent with vol_period 30.
- Outcome: price declines over the next 3 days, more after wider days -> kept: a short position graded by width, held 3 bars.
- Verdict transfer: yes: the test measures the 3-day move that follows wide days, sized by width, in falling markets only.
Forecast: One indicator: the day's high-low range as a fraction of the close, divided by the standard deviation of the last 30 daily returns (RangeInReturnStdComponent, vol_period 30). The book holds a position only on days when this ratio is 2.0 or more; that is the regime, and code adds the falling-profile vetoes. Inside the regime, the ratio is standardised against its own past 60 values (target 10, cap 20) and negated. The forecast is therefore short, about -12 at the threshold, growing towards -20 as the day gets wider. On all other days it is 0. It is never positive.
Config: 037-01_falling-market-wide-day-decline_1d_config.json
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The unusual move per case, in the short direction. A case is a short bet (a forecast rise of at least 2 points on the short side), read on the 3-bar grid. Its unusual move is minus the coin's 3-bar return from the signal's close, plus the coin's normal 3-bar drift over all windows. The measure is the mean of these unusual moves and its t, with same-day cases taken together.
- Supporting check: Split the cases at the median of |forecast|. The mean unusual move of the wider half minus that of the narrower half must be above 0.
- Confirm: The mean unusual move is positive with t of 2 or more (the price falls more than its drift after wide days), and the supporting check passes.
- Reject: The mean unusual move has t of -2 or less (the price rebounds relative to its drift after wide days).
- Inconclusive: Any t between -2 and 2, or a confirming t with the supporting check failing. Fewer than 30 cases (or fewer than 30 distinct days) is inconclusive whatever the t.
