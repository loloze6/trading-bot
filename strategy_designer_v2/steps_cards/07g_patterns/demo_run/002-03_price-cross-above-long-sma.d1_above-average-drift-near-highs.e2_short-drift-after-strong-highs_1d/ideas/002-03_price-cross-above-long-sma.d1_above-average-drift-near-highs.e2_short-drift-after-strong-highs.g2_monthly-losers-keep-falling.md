---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the more negative its 20-day return, the larger its fall over the next 5 days.
Consequence: A trader would read a sharp 20-day decline inside a long-term uptrend as continuing weakness over the next days rather than a dip to buy.
Why:
- F5: The 20-day return makes the same point. In the trending regime its lowest per-coin quintile is followed by a demeaned 5-day return of -2.06% (t -3.09, n 284), and the other four quintiles all give +0.6% to +1.1%. Its slope among negative 20-day returns is 0.130 (t 2.95, n 481).
- F1: Inside the trending regime (close above its 200-day average), 5-day returns rise steadily with the close's place in its 20-day closing range, not only in the upper half the forecast uses: the pooled slope of the coin-demeaned 5-day return on range position is 0.0335 (t 3.65, n 1402 non-overlapping cases), and on the lower half alone it is 0.0756 (t 2.78, n 527), steeper than on the upper half (0.0317, t 1.17, n 875).
