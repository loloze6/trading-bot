---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Going into the weekend, the larger a coin's 5-day return at Friday's close, the larger its rise over the next 1 day (Saturday).
Consequence: A trader would lean long into Saturday in proportion to the coin's past week's gain, and refuse to hold a coin through Saturday after a weak week.
Why:
- F1: On Saturdays, a coin's day return rises with its 5-day return up to Friday's close. The slope is 0.0645 (t=8.92, n=2382 coin-Saturdays). By quintile of that 5-day return, the mean Saturday return climbs steadily: −0.0031 (t=−1.47), 0.0007, 0.0047 (t=4.30), 0.0093 (t=4.93), 0.0111 (t=4.39).
- F2: Saturdays are the strongest day for both the coins and the book.
