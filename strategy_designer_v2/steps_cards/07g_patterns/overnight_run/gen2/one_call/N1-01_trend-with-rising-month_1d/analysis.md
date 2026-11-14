---
line: 7.g patterns
backtest: N1-01_trend-with-rising-month_1d
idea tested: N1-01_trend-with-rising-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3599 USD
---
## Findings
- **F1:** The daily close-to-close return ending on the bar stamped Saturday (all bars are stamped 00:00 UTC) averages +0.44% against about +0.07% for the other days pooled (n=2415, t=5.39); it is positive for every coin (t 1.40 to 2.92), and in 6 of 8 years (t 2.80 to 3.36 in 2019, 2020, 2024 and 2025).
- **F2:** The return on the bar stamped Friday is also positive, +0.32% (n=2411, t=3.43), so Friday and Saturday are positive for all six coins together (t 1.87 to 3.76), while Tuesday (-0.10%, t=-1.09) and Thursday (-0.18%, t=-1.67) lean negative.
- **F3:** The Friday/Saturday tilt is larger when the book is long than when it is flat. The Saturday bar returns +0.95% against +0.21% flat, and Thursday returns -0.39% against -0.09% flat, so the book's daily P&L depends partly on weekday rather than on trend.
- **F4:** After a day that falls more than 1.5 times its trailing 20-day volatility, the next day returns +0.45% to +0.78% (n=636, t=2.17 and n=267, t=1.97), against +0.11% after ordinary days. The rebound is the same whether the 20-day trend is up or down (+0.54%, t=1.84 and +0.56%, t=2.32). It is largest after sharp drops on the Thursday-stamped bar (+1.59%, n=155, t=3.63) and in XMR (+1.19%, n=162, t=3.20).
- **F5:** After a day that rises more than 2.5 times trailing volatility, the next day is flat (+0.03%, n=315, t=0.09), but the next 5 days drift up +3.86% (non-overlapping, n=65, t=2.16), against +0.57% after ordinary days.
- **F6:** The book's result rests on a few long holds. Trades closed within 10 days lose 2.7% to 4.2% on average (1567 trades), trades held over 30 days gain +98% on average (126 trades), and the top 10% of trades earn 138% of the total net P&L. ZEC alone contributes 6736 of about 11600 summed percent, and LTC is net negative.
- **F7:** The trend filter adds little forward drift. Non-overlapping forward 20-bar returns are +4.2% in active bars (n=251, t=1.77) against +1.9% and +2.3% in the two flat states (n=331 and 223, t≈1.6). The active excess is negative in 2018 (-15.4%, n=10, t=-2.44) and 2022.

## Ideas
- `N1-01_trend-with-rising-month.g1_late-week-positive-drift` (from F1, F2, F3): A coin's daily return on the bar stamped Saturday 00:00 UTC (and to a lesser degree the one stamped Friday) is higher than its average daily return. This holds across coins and years, whatever the trend state.
- `N1-01_trend-with-rising-month.g2_next-day-rebound-after-shocks` (from F4): After a coin's daily close falls by more than about one and a half times its trailing 20-day volatility, its next daily return is positive more than usual, in both up- and down-trends.
- `N1-01_trend-with-rising-month.g3_outsized-up-day-week-continuation` (from F5): After a coin closes up by more than about two and a half times its trailing 20-day volatility, it keeps rising over the following five days, even though the very next day shows no gain.
- `N1-01_trend-with-rising-month.g4_profits-live-in-long-holds` (from F6, F7): When a coin is above its 200-day average with a rising month, its long positions that survive beyond about ten days carry most of the gain, while those cut within days lose. The persistence shows up only in the multi-week holds that follow.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
