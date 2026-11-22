---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range and whose 30-day return is positive, the larger that 30-day rise, the further the coin rises over the next 5 days.
Consequence: A trader would follow strong 30-day up-trends over the next 5 days and not short the down-trends.
Why:
- F4: In the trending regime, only the top quintile of the 30-day return continued: +0.137 of a usual move (t 2.47, 433 cases). The bottom quintile gave +0.018 (t 0.33, 401 cases), so the tested idea's edge is all on the rising side.
- F5: The book's short trades lost and its long trades carried the profit.
