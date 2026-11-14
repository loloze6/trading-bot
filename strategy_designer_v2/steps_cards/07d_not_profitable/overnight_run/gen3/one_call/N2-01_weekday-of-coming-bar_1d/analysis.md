---
line: 7.d not profitable
backtest: N2-01_weekday-of-coming-bar_1d
idea tested: N2-01_weekday-of-coming-bar
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2715 USD
---
## Findings
- **F1:** The Saturday edge is only there when the coin is already rising: Friday-close-to-next-close returns average 0.0095 (t 6.57, n 1002 Fridays) when the 5-day return is positive, but −0.0019 (t −1.81, n 1054) when it is negative.
- **F2:** The book's gain before fees comes almost entirely from uptrends: active long bars make 0.0126 per bar (t 3.90, n 492) when the 20-day return is positive, but only 0.0016 (t 0.79, n 857) when it is negative, and 64% of active bars (857 of 1349) sit in the losing regime; active down20 Fridays return −0.0005 (t −0.31, n 635).
- **F3:** The book misses much of the edge it targets: Fridays left flat in an up20 regime still return 0.0049 (t 3.25, n 483), while the book holds 635 down20 Fridays that earn nothing.
- **F4:** The book is too small to pay: it is invested only on Friday bars (54.7% of Fridays, 0% on other weekdays), its mean absolute allocation is 0.075, and its mean daily return is 0.00026 against the coin's holding mean of 0.00119, so its Sharpe falls 0.09 short of holding.
- **F5:** The forecast's size carries information mainly in an uptrend: active Friday next-bar returns rise from −0.0002 to 0.0100 to 0.0169 across forecast bins 0–5, 5–10 and 10–20 when up20, but stay between −0.0019 and 0.0010 when down20; pooled, the gross forecast buckets are 0.0039 (t 2.92, n 508), 0.0032 (t 0.94, n 278) and 0.0182 (t 2.30, n 252).
- **F6:** Trades are one-day longs (1361 trades, all entered Friday, held 0.99 days, 51.7% winners) that gross 0.35% and net 0.25% each, so fees take about 29% of each trade's gain.
- **F7:** In an uptrend the drift spans several days around the weekend, not only Saturday: next-day returns when up20 are 0.0055 (t 3.74) on Thursday bars, 0.0075 (t 5.52) on Friday bars and 0.0032 (t 2.79) on Saturday bars; in down20 every weekday lies within |t| < 1.7, and Friday-to-Monday 3-day returns are 0.0115 (t 4.51, n 969 Fridays) up20 against 0.0025 (t 1.14, n 1045) down20.
- **F8:** Losses cluster in weak periods and coins: 2022 active bars average −0.0012 (t −0.56, n 235), BTC averages −0.0003 (t −0.17, n 150), and calm-volatility active bars average 0.0016 (t 1.05, n 377), against 0.0070 (t 2.03, n 375) for mid volatility.

## Ideas
- `N2-01_weekday-of-coming-bar.d1_saturday-drift-follows-recent-rise` (from F1, F2, F3, F5): A coin whose close is above its close five days earlier tends to rise from Friday's close to Saturday's close; the Saturday drift is a continuation of the recent rise rather than a calendar effect on its own.
- `N2-01_weekday-of-coming-bar.d2_uptrend-late-week-weekend-drift` (from F4, F6, F7): A coin whose close is above its close twenty days earlier tends to keep rising from Thursday's close through Monday's close, so the late-week and weekend days in an uptrend carry a positive drift.
- `N2-01_weekday-of-coming-bar.d3_forecast-size-counts-in-uptrends` (from F2, F5): When a coin is in an uptrend and its forecast of Saturday excess return is large, the Saturday bar's gain grows with the size of that forecast.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
